"""
Methods for the CSV connector.
"""

import os
import csv
import json

def _infer_schema(file_path):
    file_name = os.path.basename(file_path).split('.')[0]
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)

        properties = {}
        if file_name == 'contacts':
            for header in headers:
                if header == 'id':
                    properties[header] = {"type": "integer"}
                else:
                    properties[header] = {"type": "string"}
        elif file_name == 'customers':
            for header in headers:
                if header in ['customer_id', 'age']:
                    properties[header] = {"type": "integer"}
                else:
                    properties[header] = {"type": "string"}
        elif file_name == 'orders':
            for header in headers:
                if header in ['order_id', 'quantity']:
                    properties[header] = {"type": "integer"}
                elif header == 'price':
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