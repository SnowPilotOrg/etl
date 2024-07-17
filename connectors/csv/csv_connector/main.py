from typing import Optional

import jsonc
import typer
from rich import print
from rich.console import Console
from typing_extensions import Annotated

err_console = Console(stderr=True)
app = typer.Typer()


@app.command()
def discover(
    config_path: Annotated[str, typer.Option(help="Path to the configuration file")],
):
    """Discover available streams and their schemas."""
    typer.echo("Discovering available streams and their schemas")
    with open(config_path, "r") as file:
        config = jsonc.load(file)
    print(config)


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
