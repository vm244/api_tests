import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_post():
    response = requests.get(
        url=f"{BASE_URL}/posts/1",
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert data["id"] == 1
    assert data["userId"] == 1
    assert isinstance(data["title"], str)
    assert data["title"] != ""
    assert isinstance(data["body"], str)
    assert data["body"] != ""


def test_get_posts():
    response = requests.get(
        url=f"{BASE_URL}/posts",
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    first_post = data[0]

    assert "id" in first_post
    assert "userId" in first_post
    assert "title" in first_post
    assert "body" in first_post


def test_create_post():
    payload = {
        "title": "Test title",
        "body": "Test body",
        "userId": 1,
    }

    response = requests.post(
        url=f"{BASE_URL}/posts",
        json=payload,
        timeout=5,
    )

    assert response.status_code == 201
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert data["id"] == 101


def test_update_post():
    payload = {
        "id": 1,
        "title": "Updated title",
        "body": "Updated body",
        "userId": 1,
    }

    response = requests.put(
        url=f"{BASE_URL}/posts/1",
        json=payload,
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert data["id"] == payload["id"]
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]