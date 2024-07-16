"""
Comprehensive tests for the CSV connector methods.
"""

import json

import pytest

from csv_connector import discover, extract, load


def test_discover():
    """Test the discover method."""
    result = discover()
    assert isinstance(result, str)

    # Parse the JSON string
    data = json.loads(result)

    assert "streams" in data
    streams = data["streams"]
    assert len(streams) == 3

    stream_ids = [stream["id"] for stream in streams]
    assert "contacts" in stream_ids
    assert "customers" in stream_ids
    assert "orders" in stream_ids

    for stream in streams:
        assert "id" in stream
        assert "name" in stream
        assert "schema" in stream
        assert stream["id"] == stream["name"]
        assert "type" in stream["schema"]
        assert "properties" in stream["schema"]


def test_discover_contacts_schema():
    """Test the discover method for contacts schema."""
    result = discover()
    data = json.loads(result)

    contacts_stream = next(
        stream for stream in data["streams"] if stream["id"] == "contacts"
    )
    assert contacts_stream["schema"]["type"] == "object"
    properties = contacts_stream["schema"]["properties"]
    assert "id" in properties
    assert "name" in properties
    assert "email" in properties
    for prop in properties.values():
        assert prop["type"] == "string"


def test_discover_customers_schema():
    """Test the discover method for customers schema."""
    result = discover()
    data = json.loads(result)

    customers_stream = next(
        stream for stream in data["streams"] if stream["id"] == "customers"
    )
    assert customers_stream["schema"]["type"] == "object"
    properties = customers_stream["schema"]["properties"]
    assert "customer_id" in properties
    assert "first_name" in properties
    assert "last_name" in properties
    assert "age" in properties
    for prop, value in properties.items():
        if prop == "age":
            assert value["type"] == "integer"
        else:
            assert value["type"] == "string"


def test_discover_orders_schema():
    """Test the discover method for orders schema."""
    result = discover()
    data = json.loads(result)

    orders_stream = next(
        stream for stream in data["streams"] if stream["id"] == "orders"
    )
    assert orders_stream["schema"]["type"] == "object"
    properties = orders_stream["schema"]["properties"]
    assert "order_id" in properties
    assert "product_name" in properties
    assert "quantity" in properties
    assert "price" in properties
    for prop, value in properties.items():
        if prop in ["quantity", "price"]:
            assert value["type"] == "number"
        else:
            assert value["type"] == "string"


def test_extract_contacts():
    """Test the extract method for contacts."""
    result = extract("contacts", ["id", "name", "email"])
    assert isinstance(result, list)
    assert len(result) > 0
    assert "id" in result[0]
    assert "name" in result[0]
    assert "email" in result[0]


def test_extract_customers():
    """Test the extract method for customers."""
    result = extract("customers", ["customer_id", "first_name", "last_name", "age"])
    assert isinstance(result, list)
    assert len(result) > 0
    assert "customer_id" in result[0]
    assert "first_name" in result[0]
    assert "last_name" in result[0]
    assert "age" in result[0]


def test_extract_orders():
    """Test the extract method for orders."""
    result = extract("orders", ["order_id", "product_name", "quantity", "price"])
    assert isinstance(result, list)
    assert len(result) > 0
    assert "order_id" in result[0]
    assert "product_name" in result[0]
    assert "quantity" in result[0]
    assert "price" in result[0]


def test_load():
    """Test the load method."""
    with open("tests/contacts.csv", "r") as f:
        csv_data = f.read()
    result = load("contacts", "upsert", ["id", "name", "email"], csv_data)
    assert result is True  # Assuming successful load returns True


def test_extract_invalid_stream():
    """Test extract method with invalid stream."""
    with pytest.raises(ValueError):
        extract("invalid_stream", ["id"])


def test_load_invalid_operation():
    """Test load method with invalid operation."""
    with pytest.raises(ValueError):
        load("contacts", "invalid_operation", ["id"], "dummy_data")
