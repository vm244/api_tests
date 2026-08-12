import pytest
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.mark.smoke
def test_get_post_by_id(post_id):
    """Проверка получения одного поста по ID"""

    response = requests.get(
        url=f"{BASE_URL}/posts/{post_id}",
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert data["id"] == post_id
    assert data["userId"] == 1
    assert isinstance(data["title"], str)
    assert data["title"] != ""
    assert isinstance(data["body"], str)
    assert data["body"] != ""

def test_get_posts_list():
    """Проверка получения списка постов"""

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

@pytest.mark.smoke
def test_create_post():
    """Проверка создания нового поста"""

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

@pytest.mark.regression
def test_update_post(post_id):
    """Проверка полного обновления поста"""

    payload = {
        "id": post_id,
        "title": "Updated title",
        "body": "Updated body",
        "userId": 1,
    }

    response = requests.put(
        url=f"{BASE_URL}/posts/{post_id}",
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

@pytest.mark.regression
def test_partial_update_post(post_id):
    """Проверка частичного обновления поста"""

    payload = {
        "title": "Partially updated title",
    }

    response = requests.patch(
        url=f"{BASE_URL}/posts/{post_id}",
        json=payload,
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert data["id"] == post_id
    assert data["title"] == payload["title"]
    assert data["userId"] == 1
    assert isinstance(data["body"], str)
    assert data["body"] != ""

@pytest.mark.regression
def test_get_nonexistent_post():
    """Проверка получения несуществующего поста"""

    response = requests.get(
        url=f"{BASE_URL}/posts/999999",
        timeout=5,
    )

    assert response.status_code == 404

    with pytest.raises(requests.exceptions.HTTPError):
        response.raise_for_status()

@pytest.mark.parametrize("invalid_post_id", [0, "invalid"])
def test_get_post_with_invalid_id(invalid_post_id):
    """Проверка получения поста с некорректным ID"""

    response = requests.get(
        url=f"{BASE_URL}/posts/{invalid_post_id}",
        timeout=5,
    )

    assert response.status_code == 404

def test_get_posts_for_nonexistent_user():
    """Проверка списка постов несуществующего пользователя"""

    response = requests.get(
        url=f"{BASE_URL}/posts",
        params={"userId": 999999},
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert data == []