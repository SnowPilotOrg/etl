"""
Methods for the CSV connector.
"""

import os
import csv
import json

def discover():
    """Discover available streams and their schemas."""
    streams = []
    csv_dir = os.path.join(os.path.dirname(__file__), 'tests')

    for filename in os.listdir(csv_dir):
        if filename.endswith('.csv'):
            with open(os.path.join(csv_dir, filename), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                fields = reader.fieldnames

                schema = {
                    "type": "object",
                    "properties": {field: {"type": "string"} for field in fields}
                }

                streams.append({
                    "id": filename[:-4],  # Remove .csv extension
                    "name": filename[:-4],
                    "schema": schema
                })

    return json.dumps({"streams": streams}, indent=2)

def extract(stream_id, fields):
    """Extract data from the specified stream."""
    pass

def load(stream_id, operation, fields, data):
    """Load data into the specified stream."""
    pass

if __name__ == "__main__":
    print(discover())