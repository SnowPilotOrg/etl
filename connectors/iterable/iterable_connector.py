import httpx


def discover():
    """Discover available collections and their schemas."""
    print("hello discover")
    headers = {
        "Api-Key": "fake",
        "Content-Type": "application/json",
    }
    response = httpx.post(
        "https://api.iterable.com/api/users/update",
        headers=headers,
        json={
            "email": "jack@example.com",
            "userId": "2345",
            "dataFields": {},
            "preferUserId": True,
            "mergeNestedObjects": True,
            "createNewFields": True,
        },
    )
    print(response.json())

    # )
    # conn.request("POST", "/api/users/update", payload, headers)
    # res = conn.getresponse()
    # data = res.read()
    # print(data.decode("utf-8"))


def extract(collection_id, fields):
    """Extract data from the specified collection."""
    print("hello extract")


def load(collection_id, operation, fields, data):
    """Load data into the specified collection."""
    print("hello load")
