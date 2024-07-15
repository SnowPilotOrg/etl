"""
Comprehensive tests for the CSV connector methods.
"""

import pytest
from csv_connector import discover, extract, load

@pytest.fixture
def sample_csv_data():
    return """id,name,email
1,John Doe,john@example.com
2,Jane Smith,jane@example.com
"""

def test_discover():
    """Test the discover method."""
    result = discover()
    assert isinstance(result, list)
    assert len(result) > 0
    for stream in result:
        assert 'stream_name' in stream
        assert 'schema' in stream
        assert 'metadata' in stream

def test_extract(sample_csv_data):
    """Test the extract method."""
    result = extract('users', ['id', 'name'])
    assert isinstance(result, list)
    assert len(result) > 0
    for record in result:
        assert 'id' in record
        assert 'name' in record
        assert 'email' not in record

def test_load(sample_csv_data):
    """Test the load method."""
    result = load('users', 'upsert', ['id', 'name', 'email'], sample_csv_data)
    assert result is True  # Assuming successful load returns True

def test_extract_invalid_stream():
    """Test extract method with invalid stream."""
    with pytest.raises(ValueError):
        extract('invalid_stream', ['id'])

def test_load_invalid_operation():
    """Test load method with invalid operation."""
    with pytest.raises(ValueError):
        load('users', 'invalid_operation', ['id'], 'dummy_data')