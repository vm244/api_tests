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

@pytest.fixture
def booking_id(auth_token):
    payload = {
        "firstname": "Vadim",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-08-10",
            "checkout": "2026-08-15",
        },
        "additionalneeds": "Breakfast",
    }

    response = requests.post(
        url=f"{BASE_URL}/booking",
        json=payload,
        timeout=5,
    )

    booking_id = response.json()["bookingid"]

    yield booking_id

    requests.delete(
        url=f"{BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=5,
    )