"""
Stub methods for the CSV connector.
"""


def discover():
    """Discover available streams and their schemas."""
    print("hello discover")


def extract(stream_id, fields):
    """Extract data from the specified stream."""
    print("hello extract")


def load(stream_id, operation, fields, data):
    """Load data into the specified stream."""
    print("hello load")
