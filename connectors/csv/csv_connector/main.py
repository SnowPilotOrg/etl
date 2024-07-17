import csv
import json
import os
from typing import Dict, Optional

import jsonc
import typer
from pydantic import ValidationError, create_model
from rich import print
from rich.console import Console
from typing_extensions import Annotated

from csv_connector.models import (
    CollectionMetadata,
    Config,
    Discovery,
    Schema,
)

err_console = Console(stderr=True)
app = typer.Typer()
state: Dict[str, Optional[Config]] = {"config": None}


def infer_schema(csv_path: str, collection_id: str) -> Schema:
    """Infer the schema of the CSV file."""
    with open(csv_path, "r") as csvfile:
        headers = next(csv.reader(csvfile))
        schema = create_model(
            f"{collection_id}_schema",
            **{header: (str, ...) for header in headers},
        )

    return schema


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
    csv_path = state["config"].csv_path
    if not csv_path.endswith(".csv"):
        err_console.print(
            "[bold red]Error:[/bold red] CSV file path must end with .csv"
        )
        raise typer.Exit(code=1)

    filename = os.path.basename(csv_path)[:-4]
    schema = infer_schema(csv_path, filename)
    discovery = Discovery(
        collections=[
            CollectionMetadata(id=filename, label=filename, row=schema, upsert=schema)
        ]
    )
    print(discovery.model_dump_json(indent=2))


@app.command()
def extract():
    """Extract data from the specified collection."""
    err_console.print("Extract is not implemented yet")
    raise typer.Exit(code=1)


@app.command()
def load():
    """Load data into the specified collection."""
    err_console.print("Load is not implemented yet")
    raise typer.Exit(code=1)
