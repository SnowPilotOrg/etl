import typer

app = typer.Typer()


@app.command()
def discover():
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
