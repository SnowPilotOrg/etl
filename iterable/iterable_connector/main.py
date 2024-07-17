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
def load():
    """Load data into the specified collection."""
    raise NotImplementedError("Not implemented")