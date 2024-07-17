"""
Methods for the CSV connector.
"""

import argparse
import csv
import json
import os
import sys

import jsonc


def infer_schema(file_path, fields=None):
    with open(file_path, "r") as csvfile:
        headers = next(csv.reader(csvfile))
        selected_headers = (
            headers
            if fields is None
            else [header for header in headers if header in fields]
        )
        properties = {header: {"type": "string"} for header in selected_headers}

    return {"type": "object", "properties": properties}


def discover(config):
    collections = []
    csv_path = config["csv_path"]

    valid_csv_paths = []
    if os.path.isdir(csv_path):
        valid_csv_paths = [
            os.path.join(csv_path, filename)
            for filename in os.listdir(csv_path)
            if filename.endswith(".csv")
        ]
    elif os.path.isfile(csv_path) and csv_path.endswith(".csv"):
        valid_csv_paths = [csv_path]
    else:
        raise ValueError(f"Invalid CSV path: {csv_path}")

    for file_path in valid_csv_paths:
        filename = os.path.basename(file_path)[:-4]  # Remove .csv extension
        schema = infer_schema(file_path)
        collections.append({"id": filename, "label": filename, "schema": schema})

    return print(json.dumps({"collections": collections}, indent=2))


def extract(config, collection_id, fields):
    if not fields:
        raise ValueError("Fields are required")

    csv_path = config["csv_path"]
    file_path = (
        os.path.join(csv_path, f"{collection_id}.csv")
        if os.path.isdir(csv_path)
        else csv_path
    )

    if not os.path.isfile(file_path):
        raise ValueError(f"Invalid collection: {collection_id}")

    schema_message = {
        "type": "SCHEMA",
        "collection": collection_id,
        "schema": infer_schema(file_path, fields),
    }

    print(json.dumps(schema_message, indent=2))

    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not fields:
                break

            filtered_row = {field: row[field] for field in fields if field in row}
            record_message = {
                "type": "RECORD",
                "collection": collection_id,
                "record": filtered_row,
            }
            print(json.dumps(record_message, indent=2))

    sys.stdout.flush()


def load(config, collection_id, operation, fields, data):
    valid_operations = ["upsert", "update", "create"]
    if operation not in valid_operations:
        raise ValueError(f"Invalid operation: {operation}")

    csv_path = config["csv_path"]
    file_path = (
        os.path.join(csv_path, f"{collection_id}.csv")
        if os.path.isdir(csv_path)
        else csv_path
    )

    if not os.path.isfile(file_path):
        raise ValueError(f"Invalid collection: {collection_id}")

    # Placeholder implementation
    return json.dumps(
        {
            "success": True,
            "message": f"Data loaded into {collection_id} using {operation} operation",
        }
    )


def parse_config(config_path):
    """Parse the configuration file (supports JSONC)."""
    with open(config_path, "r") as config_file:
        return jsonc.load(config_file)


def cli():
    parser = argparse.ArgumentParser(description="CSV Connector for Snowpilot")
    parser.add_argument(
        "--config", required=True, help="Path to the configuration file"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Discover subcommand
    subparsers.add_parser("discover", help="Discover available collections")

    # Extract subcommand
    extract_parser = subparsers.add_parser("extract", help="Extract data from a collection")
    extract_parser.add_argument(
        "--collection", required=True, help="ID of the collection to extract"
    )
    extract_parser.add_argument("--fields", nargs="+", help="Fields to extract")

    # Load subcommand
    load_parser = subparsers.add_parser("load", help="Load data into a collection")
    load_parser.add_argument(
        "--collection", required=True, help="ID of the collection to load data into"
    )
    load_parser.add_argument(
        "--operation",
        choices=["upsert", "update", "create"],
        required=True,
        help="Operation to perform",
    )
    load_parser.add_argument(
        "--fields",
        nargs="+",
        help="Fields to load",
    )

    args = parser.parse_args()
    config = parse_config(args.config)

    if args.command == "discover":
        discover(config)
    elif args.command == "extract":
        extract(config, args.collection, args.fields)
    elif args.command == "load":
        data = json.loads(sys.stdin.read())
        load(config, args.collection, args.operation, args.fields, data)
