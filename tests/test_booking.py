import requests

def test_create_auth_token(base_url):
    """Проверка получения токена авторизации"""

    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(
        url=f"{base_url}/auth",
        json=payload,
        timeout=5,
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    data = response.json()

    assert "token" in data
    assert isinstance(data["token"], str)
    assert data["token"] != ""

def test_create_booking(base_url, deposit_paid, api_client):
    """Проверка создания бронирования"""

    payload = {
        "firstname": "Vadim",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": deposit_paid,
        "bookingdates": {
            "checkin": "2026-08-10",
            "checkout": "2026-08-15",
        },
        "additionalneeds": "Breakfast",
    }

    response = api_client.post(
        url=f"{base_url}/booking",
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

def test_get_booking_by_id(booking_id, base_url, api_client):
    """Проверка получения бронирования по ID"""

    response = api_client.get(
        url=f"{base_url}/booking/{booking_id}",
        timeout=5,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["firstname"] == "Vadim"
    assert data["lastname"] == "Test"

def test_update_booking(booking_id, auth_token, base_url, api_client):
    """Проверка полного обновления бронирования"""

    payload = {
        "firstname": "Vadim",
        "lastname": "Updated",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-08-10",
            "checkout": "2026-08-20",
        },
        "additionalneeds": "Dinner",
    }

    api_client.cookies.set("token", auth_token)

    response = api_client.put(
        url=f"{base_url}/booking/{booking_id}",
        json=payload,
        timeout=5,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["firstname"] == payload["firstname"]
    assert data["lastname"] == payload["lastname"]
    assert data["totalprice"] == payload["totalprice"]
    assert data["depositpaid"] == payload["depositpaid"]
    assert data["bookingdates"] == payload["bookingdates"]
    assert data["additionalneeds"] == payload["additionalneeds"]