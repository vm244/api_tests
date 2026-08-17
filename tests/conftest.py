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
def api_client():
    session = requests.Session()

    session.headers.update({
        "Accept": "application/json",
    })

    yield session

    session.close()

@pytest.fixture(scope="session")
def auth_token(base_url, api_client):
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

    return response.json()["token"]

@pytest.fixture(scope="session")
def authorized_api_client(auth_token):
    session = requests.Session()

    session.headers.update({
        "Accept": "application/json",
    })

    session.cookies.set("token", auth_token)

    yield session

    session.close()

@pytest.fixture
def booking_payload():
    return {
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

@pytest.fixture
def booking_id(
    api_client,
    authorized_api_client,
    base_url,
    request,
    booking_payload,
):
    response = api_client.post(
        url=f"{base_url}/booking",
        json=booking_payload,
        timeout=5,
    )

    booking_id = response.json()["bookingid"]

    yield booking_id

    if getattr(request.node, "test_failed", False):
        print(f"\nTEST FAILED: booking_id={booking_id}")

    authorized_api_client.delete(
        url=f"{base_url}/booking/{booking_id}",
        timeout=5,
    )

def pytest_collection_modifyitems(items):
    print("\nCOLLECTED TESTS:")

    for item in items:
        print(item.name)

@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item):
    report = yield

    if report.when == "call":
        item.test_failed = report.failed

    return report
