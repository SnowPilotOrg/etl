"""
Stub methods for the CSV connector.
"""

def discover():
    """Discover available streams and their schemas."""
    pass

def extract(stream_id, fields):
    """Extract data from the specified stream."""
    import csv
    import json
    import os

    try:
        with open(f"{stream_id}.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)

            # Generate and output SCHEMA message
            schema = {
                "type": "SCHEMA",
                "stream": stream_id,
                "schema": {
                    "type": "object",
                    "properties": {field: {"type": "string"} for field in reader.fieldnames}
                },
                "key_properties": []  # Assuming no primary key for simplicity
            }
            print(json.dumps(schema))

            # Generate and output RECORD messages
            for row in reader:
                record = {
                    "type": "RECORD",
                    "stream": stream_id,
                    "record": row
                }
                print(json.dumps(record))
    except FileNotFoundError:
        print(f"Error: CSV file '{stream_id}.csv' not found.")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")

def load(stream_id, operation, fields, data):
    """Load data into the specified stream."""
    pass