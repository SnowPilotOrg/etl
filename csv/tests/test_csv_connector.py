"""
Simple tests for the CSV connector stub methods.
"""

from csv_connector import discover, extract, load

def test_discover():
    """Test the discover method."""
    assert discover() is None

def test_extract():
    """Test the extract method."""
    assert extract('dummy_stream', ['field1', 'field2']) is None

def test_load():
    """Test the load method."""
    assert load('dummy_stream', 'upsert', ['field1', 'field2'], 'dummy_data') is None