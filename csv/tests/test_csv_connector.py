"""
Comprehensive tests for the CSV connector methods.
"""

import json

import pytest

from src import discover, extract, load


def test_discover():
    """Test the discover method."""
    result = discover()
    assert isinstance(result, str)

    # Parse the JSON string
    data = json.loads(result)

    assert "collections" in data
    collections = data["collections"]
    assert len(collections) == 3

    collection_ids = [collection["id"] for collection in collections]
    assert "contacts" in collection_ids
    assert "customers" in collection_ids
    assert "orders" in collection_ids

    for collection in collections:
        assert "id" in collection
        assert "name" in collection
        assert "schema" in collection
        assert collection["id"] == collection["name"]
        assert "type" in collection["schema"]
        assert "properties" in collection["schema"]


def test_discover_contacts_schema():
    """Test the discover method for contacts schema."""
    result = discover()
    data = json.loads(result)

    contacts_collection = next(
        collection for collection in data["collections"] if collection["id"] == "contacts"
    )
    assert contacts_collection["schema"]["type"] == "object"
    properties = contacts_collection["schema"]["properties"]
    assert "id" in properties
    assert "name" in properties
    assert "email" in properties
    for prop in properties.values():
        assert prop["type"] == "string"


def test_discover_customers_schema():
    """Test the discover method for customers schema."""
    result = discover()
    data = json.loads(result)

    customers_collection = next(
        collection for collection in data["collections"] if collection["id"] == "customers"
    )
    assert customers_collection["schema"]["type"] == "object"
    properties = customers_collection["schema"]["properties"]
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

    orders_collection = next(
        collection for collection in data["collections"] if collection["id"] == "orders"
    )
    assert orders_collection["schema"]["type"] == "object"
    properties = orders_collection["schema"]["properties"]
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


def test_extract_invalid_collection():
    """Test extract method with invalid collection."""
    with pytest.raises(ValueError):
        extract("invalid_collection", ["id"])


def test_load_invalid_operation():
    """Test load method with invalid operation."""
    with pytest.raises(ValueError):
        load("contacts", "invalid_operation", ["id"], "dummy_data")
