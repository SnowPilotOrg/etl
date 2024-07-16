import httpx


def discover():
    """Discover available streams and their schemas."""
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


def extract(stream_id, fields):
    """Extract data from the specified stream."""
    print("hello extract")


def load(stream_id, operation, fields, data):
    """Load data into the specified stream."""
    print("hello load")
