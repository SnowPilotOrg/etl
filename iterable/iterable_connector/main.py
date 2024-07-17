import json
import sys
from datetime import datetime
from typing import Dict, Optional

import httpx
import jsonc
import typer
from pydantic import ValidationError, create_model
from rich import print
from rich.console import Console
from typing_extensions import Annotated

from iterable_connector.models import (
    Catalog,
    CollectionMetadata,
    Config,
    Schema,
    User,
)

err_console = Console(stderr=True)
app = typer.Typer()
state: Dict[str, Optional[Config]] = {"config": None}


# OPEN Q: Should we have a `meta` command to get the schema of the config file?


def build_client(config: Config):
    return httpx.Client(
        # NOTE: base_url will have to be dynamic when we support eu-region accounts
        base_url="https://api.iterable.com/api/",
        headers={
            "Api-Key": config.api_key,
            "User-Agent": "Snowpilot/1.0 (developers@snowpilot.com)",
        },
    )


def api_type_to_pydantic_type(type: str) -> type:
    match type:
        case "string":
            return str
        case "long":
            return int
        case "boolean":
            return bool
        case "date":
            return datetime
        case "object":
            return dict
        case _:
            raise ValueError(f"Unsupported type: {type}")


def get_user_schema(config: Config) -> Schema:
    with build_client(config) as client:
        response = client.get("users/getFields")
        response.raise_for_status()

        # Example response
        # {
        #  "fields": {
        #     "devices.appBuild": "string",
        #     "my_custom_field": "string",
        #     "phoneNumberDetails.carrier": "string",
        #     "phoneNumber": "string",
        #     "email": "string",
        #     ...
        #   }
        # }

        response_body = response.json()
        fields = response_body["fields"]

        schema = create_model(
            "user_schema",
            **{
                field: (api_type_to_pydantic_type(type), ...)
                # TODO: these aren't all required. Fix the pydantic model
                for (field, type) in fields.items()
            },
        )
        return schema


@app.callback()
def config(
    config_file: Annotated[
        typer.FileText,
        typer.Option("--config", "-f", help="Path to the configuration file"),
    ],
):
    """Provide the path to the configuration file."""
    raw_config = jsonc.load(config_file)
    try:
        validated_config = Config.model_validate(raw_config)
        state["config"] = validated_config
    except ValidationError as e:
        err_console.print("[bold red]Error in configuration file:[/bold red]")
        err_console.print(e)
        raise typer.Exit(code=1)


@app.command()
def discover():
    """Discover available collections and their schemas."""
    user_schema = get_user_schema(state["config"])
    catalog = Catalog(
        collections=[
            CollectionMetadata(
                id="users", label="Users", row=user_schema, upsert=User
            )  # TODO: we should enforce the types of custom fields on upsert
        ]
    )
    print(catalog.model_dump_json(indent=2))


@app.command()
def extract(collection_id: Annotated[str, typer.Option("--collection", "-c")]):
    """Extract data from the specified collection."""
    if collection_id not in ["users"]:
        raise typer.BadArgument("Unsupported collection ID")

    with build_client(state["config"]) as client:
        response = client.get(
            "export/data.json",
            params={"dataTypeName": "user", "range": "All"},
        )
        response.raise_for_status()
        print(response.text.strip())


@app.command()
def load(
    collection_id: Annotated[str, typer.Option("--collection", "-c")],
    operation: Annotated[str, typer.Option("--operation", "-o")],
):
    """Load data into the specified collection."""
    # TODO: support collections other than users, and list which ones are valid
    if collection_id not in ["users"]:
        raise typer.BadArgument("Unsupported collection ID")

    # TODO: support other operations, and list the valid ones
    if operation not in ["upsert"]:
        raise typer.BadArgument("Unsupported operation")

    records: list[Dict] = []

    # Read JSONL from stdin
    # TODO: we should do this in a streaming fashion
    for line in sys.stdin:
        try:
            record = json.loads(line.strip())
            records.append(record)
        except json.JSONDecodeError:
            err_console.print(
                f"[bold yellow]Warning: Skipping invalid JSON line: {line.strip()}[/bold yellow]"
            )

    if not records:
        err_console.print(
            "[bold yellow]Warning: No valid records found in input.[/bold yellow]"
        )
        return

        # TODO: rate-limiting & size-limiting
        # TODO: error handling

    # https://api.iterable.com/api/docs#users_bulkUpdateUser
    body = {
        "users": [
            {**record, "preferUserId": True, "mergeNestedObjects": True}
            for record in records
        ]
    }

    with build_client(state["config"]) as client:
        response = client.post(
            "users/bulkUpdate",
            json=body,
        )
        response.raise_for_status()
        print(response.json())

    print(
        f"[green]Successfully loaded {len(records)} records into {collection_id}[/green]"
    )
