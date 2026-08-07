import pytest
import requests

@pytest.fixture
def post_id():
    return 1

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture
def auth_token():
    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        url=f"{BASE_URL}/auth",
        json=payload,
        timeout=5,
    )

    data = response.json()

    return data["token"]