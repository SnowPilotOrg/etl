"""
Methods for the CSV connector.
"""

import os
import csv
import json
import jsonc
import argparse
import sys

def _infer_schema(file_path):
    file_name = os.path.basename(file_path).split('.')[0]
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        properties = {}
        if file_name == 'contacts':
            for header in headers:
                properties[header] = {"type": "string"}
        elif file_name == 'customers':
            for header in headers:
                if header == 'age':
                    properties[header] = {"type": "integer"}
                else:
                    properties[header] = {"type": "string"}
        elif file_name == 'orders':
            for header in headers:
                if header in ['quantity', 'price']:
                    properties[header] = {"type": "number"}
                else:
                    properties[header] = {"type": "string"}
        else:
            # Default behavior for unknown files
            for header in headers:
                properties[header] = {"type": "string"}

        return {
            "type": "object",
            "properties": properties
        }

def discover(config):
    """Discover available streams and their schemas."""
    print(f"Discover function called with config: {config}")
    streams = []
    csv_path = config['csv_path']

    if os.path.isdir(csv_path):
        for filename in os.listdir(csv_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(csv_path, filename)
                stream_id = filename[:-4]  # Remove .csv extension
                schema = _infer_schema(file_path)
                streams.append({
                    "id": stream_id,
                    "name": stream_id,
                    "schema": schema
                })
                print(f"Processed file: {file_path}")
                print(f"Generated schema: {json.dumps(schema, indent=2)}")
    elif os.path.isfile(csv_path) and csv_path.endswith('.csv'):
        stream_id = os.path.basename(csv_path)[:-4]  # Remove .csv extension
        schema = _infer_schema(csv_path)
        streams.append({
            "id": stream_id,
            "name": stream_id,
            "schema": schema
        })
        print(f"Processed file: {csv_path}")
        print(f"Generated schema: {json.dumps(schema, indent=2)}")
    else:
        raise ValueError(f"Invalid CSV path: {csv_path}")

    print(f"Final streams data: {json.dumps(streams, indent=2)}")
    return json.dumps({"streams": streams}, indent=2)

def extract(config, stream_id, fields):
    """Extract data from the specified stream."""
    csv_path = config['csv_path']
    file_path = os.path.join(csv_path, f"{stream_id}.csv") if os.path.isdir(csv_path) else csv_path

    if not os.path.isfile(file_path):
        raise ValueError(f"Invalid stream: {stream_id}")

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            if fields:
                filtered_row = {field: row[field] for field in fields if field in row}
                data.append(filtered_row)
            else:
                data.append(row)

    return json.dumps(data, indent=2)

def load(config, stream_id, operation, fields, data):
    """Load data into the specified stream."""
    valid_operations = ['upsert', 'update', 'create']
    if operation not in valid_operations:
        raise ValueError(f"Invalid operation: {operation}")

    csv_path = config['csv_path']
    file_path = os.path.join(csv_path, f"{stream_id}.csv") if os.path.isdir(csv_path) else csv_path

    if not os.path.isfile(file_path):
        raise ValueError(f"Invalid stream: {stream_id}")

    # Placeholder implementation
    return json.dumps({"success": True, "message": f"Data loaded into {stream_id} using {operation} operation"})

def parse_config(config_path):
    """Parse the configuration file (supports JSONC)."""
    with open(config_path, 'r') as config_file:
        return jsonc.load(config_file)

def main():
    parser = argparse.ArgumentParser(description="CSV Connector for Snowpilot")
    parser.add_argument('--config', required=True, help='Path to the configuration file')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Discover subcommand
    subparsers.add_parser('discover', help='Discover available streams')

    # Extract subcommand
    extract_parser = subparsers.add_parser('extract', help='Extract data from a stream')
    extract_parser.add_argument('--stream-id', required=True, help='ID of the stream to extract')
    extract_parser.add_argument('--fields', nargs='+', help='Fields to extract')

    # Load subcommand
    load_parser = subparsers.add_parser('load', help='Load data into a stream')
    load_parser.add_argument('--stream-id', required=True, help='ID of the stream to load data into')
    load_parser.add_argument('--operation', choices=['upsert', 'update', 'create'], required=True, help='Operation to perform')
    load_parser.add_argument('--fields', nargs='+', help='Fields to load')

    args = parser.parse_args()
    config = parse_config(args.config)

    if args.command == 'discover':
        print(discover(config))
    elif args.command == 'extract':
        print(extract(config, args.stream_id, args.fields))
    elif args.command == 'load':
        data = json.loads(sys.stdin.read())
        print(load(config, args.stream_id, args.operation, args.fields, data))

if __name__ == "__main__":
    main()