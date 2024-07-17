import csv
import json
import os
import sys
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
    csv_path = state["config"].csv_path
    filename = os.path.basename(csv_path)[:-4]
    schema = infer_schema(csv_path, filename)
    discovery = Discovery(
        collections=[
            CollectionMetadata(id=filename, label=filename, row=schema, insert=schema)
        ]
    )
    print(discovery.model_dump_json(indent=2))


@app.command()
def extract():
    """Extract data from the specified collection."""
    csv_path = state["config"].csv_path
    with open(csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)


@app.command()
def load():
    """Load data into the specified collection."""
    config = state["config"]
    if not config:
        err_console.print("[bold red]Error: Configuration not loaded.[/bold red]")
        raise typer.Exit(code=1)

    csv_path = config.csv_path
    records: list[Dict] = []

    # Read JSONL from stdin
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

    # Write records to CSV
    fieldnames = records[0].keys()
    with open(csv_path, "a+", newline="") as csvfile:
        # Check if file is empty
        csvfile.seek(0, 2)
        is_empty = csvfile.tell() == 0
        # If not empty, check if last character is newline
        if not is_empty:
            csvfile.seek(0)
            content = csvfile.read()
            if content and content[-1] != "\n":
                csvfile.write("\n")

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if file is empty
        if is_empty:
            writer.writeheader()

        for record in records:
            writer.writerow(record)

    print(f"[green]Successfully loaded {len(records)} records into {csv_path}[/green]")
