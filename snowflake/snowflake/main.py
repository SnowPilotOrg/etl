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

from snowflake.models import (
    Catalog,
    CollectionMetadata,
    Config,
    Schema,
    User,
)

err_console = Console(stderr=True)
app = typer.Typer()
state: Dict[str, Optional[Config]] = {"config": None}


def build_client(config: Config):
    raise NotImplementedError("build_client not implemented")


def api_type_to_pydantic_type(type: str) -> type:
    raise NotImplementedError("api_type_to_pydantic_type not implemented")
    # match type:
    #     case "string":
    #         return str
    #     case "long":
    #         return int
    #     case "boolean":
    #         return bool
    #     case "date":
    #         return datetime
    #     case "object":
    #         return dict
    #     case _:
    #         raise ValueError(f"Unsupported type: {type}")


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
    raise NotImplementedError("Discover operation not implemented")


@app.command()
def extract(collection_id: Annotated[str, typer.Option("--collection", "-c")]):
    """Extract data from the specified collection."""
    raise NotImplementedError("Extract operation not implemented")


@app.command()
def load(
    collection_id: Annotated[str, typer.Option("--collection", "-c")],
    operation: Annotated[str, typer.Option("--operation", "-o")],
):
    """Load data into the specified collection."""
    raise NotImplementedError("Load operation not implemented")
