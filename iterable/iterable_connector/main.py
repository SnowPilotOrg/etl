import asyncio
import json
import os
import sys
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


@app.callback()
def config(
    config_file: Annotated[
        typer.FileText,
        typer.Option("--config", "-c", help="Path to the configuration file"),
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
    catalog = Catalog(
        collections=[CollectionMetadata(id="users", label="Users", upsert=User)]
    )
    print(catalog.model_dump_json(indent=2))


@app.command()
def extract():
    """Extract data from the specified collection."""
    response = httpx.get(
        "https://api.iterable.com/api/export/data.json",
        params={"dataTypeName": "user", "range": "All"},
        headers={"Api-Key": state["config"].api_key},
    )
    print(response.text.strip())


@app.command()
def load(
    collection_id: Annotated[str, typer.Option("--collection")],
    operation: Annotated[str, typer.Option("--operation")],
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
    response = httpx.post(
        "https://api.iterable.com/api/users/bulkUpdate",
        headers={"Api-Key": state["config"].api_key},
        json=body,
    )
    print(response.json())

    print(
        f"[green]Successfully loaded {len(records)} records into {collection_id}[/green]"
    )
