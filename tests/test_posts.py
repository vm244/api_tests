import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_post():
    response = requests.get(
        url=f"{BASE_URL}/posts/1",
        timeout=5,
    )

    data = response.json()

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    assert data["id"] == 1
    assert data["userId"] == 1
    assert isinstance(data["title"], str)
    assert data["title"] != ""
    assert isinstance(data["body"], str)
    assert data["body"] != ""

