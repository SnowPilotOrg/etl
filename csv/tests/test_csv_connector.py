"""
Comprehensive tests for the CSV connector methods.
"""

import pytest
from csv_connector import discover, extract, load

def test_discover():
    """Test the discover method."""
    result = discover()
    assert isinstance(result, list)
    assert len(result) == 3
    stream_names = [stream['stream_name'] for stream in result]
    assert 'contacts' in stream_names
    assert 'customers' in stream_names
    assert 'orders' in stream_names

def test_extract_contacts():
    """Test the extract method for contacts."""
    result = extract('contacts', ['id', 'name', 'email'])
    assert isinstance(result, list)
    assert len(result) > 0
    assert 'id' in result[0]
    assert 'name' in result[0]
    assert 'email' in result[0]

def test_extract_customers():
    """Test the extract method for customers."""
    result = extract('customers', ['customer_id', 'first_name', 'last_name', 'age'])
    assert isinstance(result, list)
    assert len(result) > 0
    assert 'customer_id' in result[0]
    assert 'first_name' in result[0]
    assert 'last_name' in result[0]
    assert 'age' in result[0]

def test_extract_orders():
    """Test the extract method for orders."""
    result = extract('orders', ['order_id', 'product_name', 'quantity', 'price'])
    assert isinstance(result, list)
    assert len(result) > 0
    assert 'order_id' in result[0]
    assert 'product_name' in result[0]
    assert 'quantity' in result[0]
    assert 'price' in result[0]

def test_load():
    """Test the load method."""
    with open('tests/contacts.csv', 'r') as f:
        csv_data = f.read()
    result = load('contacts', 'upsert', ['id', 'name', 'email'], csv_data)
    assert result is True  # Assuming successful load returns True

def test_extract_invalid_stream():
    """Test extract method with invalid stream."""
    with pytest.raises(ValueError):
        extract('invalid_stream', ['id'])

def test_load_invalid_operation():
    """Test load method with invalid operation."""
    with pytest.raises(ValueError):
        load('contacts', 'invalid_operation', ['id'], 'dummy_data')