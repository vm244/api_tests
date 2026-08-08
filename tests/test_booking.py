import requests


BASE_URL = "https://restful-booker.herokuapp.com"


def test_create_auth_token():
    """Проверка получения токена авторизации"""

    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        url=f"{BASE_URL}/auth",
        json=payload,
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert "token" in data
    assert isinstance(data["token"], str)
    assert data["token"] != ""

def test_create_booking():
    """Проверка создания бронирования"""

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

    assert response.status_code == 200

    data = response.json()

    assert "bookingid" in data
    assert "booking" in data

    booking = data["booking"]

    assert booking["firstname"] == payload["firstname"]
    assert booking["lastname"] == payload["lastname"]
    assert booking["totalprice"] == payload["totalprice"]
    assert booking["depositpaid"] == payload["depositpaid"]
    assert booking["bookingdates"] == payload["bookingdates"]
    assert booking["additionalneeds"] == payload["additionalneeds"]

def test_get_booking_by_id(booking_id):
    """Проверка получения бронирования по ID"""

    response = requests.get(
        url=f"{BASE_URL}/booking/{booking_id}",
        timeout=5,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["firstname"] == "Vadim"
    assert data["lastname"] == "Test"