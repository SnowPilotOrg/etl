from typing import Optional

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def discover(
    config: Annotated[str, typer.Option(help="Path to the configuration file")],
):
    """Discover available streams and their schemas."""
    typer.echo("Discovering available streams and their schemas")


@app.command()
def extract():
    """Extract data from the specified stream."""
    typer.echo("Extracting data from the specified stream")


@app.command()
def load():
    """Load data into the specified stream."""
    typer.echo("Loading data into the specified stream")
