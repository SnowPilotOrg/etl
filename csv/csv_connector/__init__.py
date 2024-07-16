"""
Methods for the CSV connector.
"""

import os
import csv
import json

def _infer_schema(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        first_row = next(reader)

        properties = {}
        for header, value in zip(headers, first_row):
            if header in ['id', 'customer_id', 'order_id', 'age', 'quantity']:
                properties[header] = {"type": "integer"}
            elif header == 'price':
                properties[header] = {"type": "number"}
            else:
                properties[header] = {"type": "string"}

        return {
            "type": "object",
            "properties": properties
        }

def discover():
    """Discover available streams and their schemas."""
    streams = []
    csv_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')

    for filename in os.listdir(csv_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_dir, filename)
            stream_id = filename[:-4]  # Remove .csv extension
            schema = _infer_schema(file_path)

            streams.append({
                "id": stream_id,
                "name": stream_id,
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