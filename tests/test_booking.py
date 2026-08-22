import pytest


def test_create_auth_token(base_url, api_client):
    """Проверка получения токена авторизации"""

    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = api_client.post(
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


@pytest.mark.smoke
@pytest.mark.parametrize("deposit_paid", [True, False])
def test_create_booking(base_url, deposit_paid, api_client, booking_payload):
    """Проверка создания бронирования"""

    booking_payload["depositpaid"] = deposit_paid

    response = api_client.post(
        url=f"{base_url}/booking",
        json=booking_payload,
        timeout=5,
    )

    assert response.status_code == 200

    data = response.json()

    assert "bookingid" in data
    assert "booking" in data

    booking = data["booking"]

    assert booking["firstname"] == booking_payload["firstname"]
    assert booking["lastname"] == booking_payload["lastname"]
    assert booking["totalprice"] == booking_payload["totalprice"]
    assert booking["depositpaid"] == booking_payload["depositpaid"]
    assert booking["bookingdates"] == booking_payload["bookingdates"]
    assert booking["additionalneeds"] == booking_payload["additionalneeds"]


def test_get_booking_by_id(
    booking_id,
    base_url,
    api_client,
    booking_payload,
):
    """Проверка получения бронирования по ID"""

    response = api_client.get(
        url=f"{base_url}/booking/{booking_id}",
        timeout=5,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["firstname"] == booking_payload["firstname"]
    assert data["lastname"] == booking_payload["lastname"]


def test_update_booking(booking_id, base_url, authorized_api_client):
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

    response = authorized_api_client.put(
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


def test_partial_update_booking(
    booking_id,
    base_url,
    authorized_api_client,
):
    """Проверка частичного обновления бронирования"""

    payload = {
        "firstname": "Updated",
    }

    response = authorized_api_client.patch(
        url=f"{base_url}/booking/{booking_id}",
        json=payload,
        timeout=5,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["firstname"] == payload["firstname"]
    assert data["lastname"] == "Test"


def test_delete_booking(
    base_url,
    api_client,
    authorized_api_client,
    booking_payload,
):
    """Проверка удаления бронирования"""

    create_response = api_client.post(
        url=f"{base_url}/booking",
        json=booking_payload,
        timeout=5,
    )

    assert create_response.status_code == 200

    booking_id = create_response.json()["bookingid"]

    delete_response = authorized_api_client.delete(
        url=f"{base_url}/booking/{booking_id}",
        timeout=5,
    )

    assert delete_response.status_code == 201

    get_response = api_client.get(
        url=f"{base_url}/booking/{booking_id}",
        timeout=5,
    )

    assert get_response.status_code == 404
