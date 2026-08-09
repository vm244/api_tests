import pytest
import requests

@pytest.fixture
def post_id():
    return 1

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://restful-booker.herokuapp.com",
        help="API base URL",
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture(scope="session")
def auth_token(base_url):

    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        url=f"{base_url}/auth",
        json=payload,
        timeout=5,
    )

    return response.json()["token"]

@pytest.fixture
def booking_id(auth_token, base_url):

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
        url=f"{base_url}/booking",
        json=payload,
        timeout=5,
    )

    booking_id = response.json()["bookingid"]

    yield booking_id

    requests.delete(
        url=f"{base_url}/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=5,
    )