"""
Stub methods for the CSV connector.
"""


def discover():
    """Discover available streams and their schemas."""
    pass


def extract(stream_id, fields):
    """Extract data from the specified stream."""
    pass


def load(stream_id, operation, fields, data):
    """Load data into the specified stream."""
    pass
