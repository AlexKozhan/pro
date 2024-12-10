import pytest
from API.random_data import generate_email, generate_string
from logger import logger
from typing import Generator
import json
import time
from playwright.sync_api import Playwright, APIRequestContext

MAIN_URL = "https://thinking-tester-contact-list.herokuapp.com"

user_data = {
    "email": "Aleksmason@gmail.com",
    "password": "sangvin123"
}

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url=MAIN_URL)
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def auth_token(api_request_context: APIRequestContext):
    """Login as user and get token."""
    response = api_request_context.post("/users/login", data=json.dumps(user_data), headers={"Content-Type": "application/json"})
    if response.status == 200:
        return response.json().get("token")
    else:
        # Log the response details for debugging
        print(f"Authorization failed: {response.status}, {response.text()}")
        raise RuntimeError(f"Ошибка авторизации: {response.status}, {response.text()}")

@pytest.fixture(scope="session")
def base_url():
    """Fixture to easify test_api code"""
    return MAIN_URL

@pytest.fixture(scope="function")
def cleanup_contacts(auth_token, api_request_context: APIRequestContext):
    """Fixture delete contacts after tests"""
    yield
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = api_request_context.get("/contacts", headers=headers)
    contacts = response.json()

    for contact in contacts:
        contact_id = contact["_id"]
        api_request_context.delete(f"/contacts/{contact_id}", headers=headers)

@pytest.fixture(scope="function")
def register_user(api_request_context: APIRequestContext):
    """Fixture to register a user and return user details including email."""
    url = "/users"
    first_name = generate_string(3, 6)
    last_name = generate_string(5, 10)
    email = generate_email()
    body = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": "Tester11"
    }
    response = api_request_context.post(url, data=json.dumps(body), headers={"Content-Type": "application/json"})
    response_json = response.json()
    return {
        "user": response_json.get("user"),
        "token": response_json.get("token"),
        "email": email  # Include the email in the returned dictionary
    }


@pytest.fixture(scope="function")
def user_with_token(register_user, api_request_context: APIRequestContext):
    """Register user and get token."""
    u_data = register_user
    user_info = u_data['user']
    login_body = {
        "email": user_info["email"],
        "password": "Tester11"  # Use the same password used during registration
    }
    logger.info(f"Logging in with body: {login_body}")

    max_retries = 1
    for attempt in range(max_retries):
        response = api_request_context.post(
            "/users/login",
            data=json.dumps(login_body),
            headers={"Content-Type": "application/json"},
            timeout=60000  # Increase timeout to 60 seconds
        )

        if response.status == 200:
            logger.info(f"Login response status: {response.status}, Response body: {response.json()}")
            return response.json()
        else:
            logger.error(f"Login failed with status: {response.status}, Response body: {response.text()}")
            if attempt < max_retries - 1:
                logger.info("Retrying login...")
                time.sleep(5)  # Wait for 5 seconds before retrying

    raise Exception(f"Login failed with status: {response.status} after {max_retries} attempts")

@pytest.fixture(scope="function")
def created_contact(auth_token, api_request_context: APIRequestContext):
    """Fixture create contact"""
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "birthdate": "1970-01-01",
        "email": "jdoe@fake.com",
        "phone": "8005555555",
        "street1": "1 Main St.",
        "street2": "Apartment A",
        "city": "Anytown",
        "stateProvince": "KS",
        "postalCode": "12345",
        "country": "USA"
    }

    response = api_request_context.post("/contacts", data=json.dumps(body), headers=headers)
    data = response.json()
    contact_id = data["_id"]
    return contact_id