import csv
from typing import Optional

import jsonc
import typer
from rich import print
from rich.console import Console
from typing_extensions import Annotated

err_console = Console(stderr=True)
app = typer.Typer()
state = {"config": None}


def infer_schema(csv_path: str, fields: Optional[list[str]] = None) -> dict:
    """Infer the schema of the CSV file."""
    with open(csv_path, "r") as csvfile:
        headers = next(csv.reader(csvfile))
        selected_headers = (
            headers
            if fields is None
            else [header for header in headers if header in fields]
        )
        properties = {header: {"type": "string"} for header in selected_headers}

    return {"type": "object", "properties": properties}


# OPEN Q: Meta command? Get the schema of the config file


@app.callback()
def config(
    config_file: Annotated[
        typer.FileText,
        typer.Option("--config", "-c", help="Path to the configuration file"),
    ],
):
    """Provide the path to the configuration file."""
    config = jsonc.load(config_file)
    # TODO: Validate the config before setting it
    state["config"] = config


@app.command()
def discover():
    """Discover available streams and their schemas."""
    csv_path = state["config"]["csv_path"]
    print(csv_path)


@app.command()
def extract():
    """Extract data from the specified stream."""
    err_console.print("Extract is not implemented yet")
    raise typer.Exit(code=1)


@app.command()
def load():
    """Load data into the specified stream."""
    err_console.print("Load is not implemented yet")
    raise typer.Exit(code=1)
