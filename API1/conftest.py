"""
Fixtures for API tests, including authorization
and data cleaning.
"""
import pytest
import requests
from API.random_data import generate_email, generate_string
from API import test_data

MAIN_URL = "https://thinking-tester-contact-list.herokuapp.com"

user_data = {
    "email": "Aleksmason@gmail.com",
    "password": "sangvin123"
}


@pytest.fixture(scope="session")
def auth_token():
    """Login as user and get token."""
    response = requests.post(f"{MAIN_URL}/users/login", json=user_data)
    if response.status_code == 200:
        return response.json().get("token")
    raise RuntimeError(f"Ошибка авторизации: "
                       f"{response.status_code}, {response.text}")


@pytest.fixture(scope="session")
def base_url():
    """Fixture to easify test_api code"""
    return MAIN_URL


@pytest.fixture(scope="function")
def cleanup_contacts(auth_token, base_url):
    """Fixture delete contacts after tests"""
    yield
    url = f"{base_url}/contacts"
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(url, headers=headers)
    contacts = response.json()

    for contact in contacts:
        contact_id = contact["_id"]
        delete_url = f"{base_url}/contacts/{contact_id}"
        requests.delete(delete_url, headers=headers)


@pytest.fixture(scope="function")
def register_user(base_url):
    """Fixture register user"""
    url = f"{base_url}/users"
    first_name = generate_string(3, 6)
    last_name = generate_string(5, 10)
    email = generate_email()
    body = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": "Tester11"
    }
    response = requests.post(url, json=body)
    test_data.u_email = response.json().get("user").get("email")
    u_data = response.json().get("user")
    return {
        "email": u_data.get("email"),
        "password": "Tester11"
    }


@pytest.fixture(scope="function")
def user_with_token(register_user, base_url):
    """Register user and get token."""
    u_data = register_user
    response = requests.post(f"{base_url}/users/login", json={
        "email": u_data["email"],
        "password": u_data["password"]
    })
    if response.status_code == 200:
        token = response.json().get("token")
        return {
            "user": user_data,
            "token": token
        }
    raise RuntimeError(f"Authorization error: {response.status_code},"
                       f" {response.text}")


@pytest.fixture(scope="function")
def created_contact(auth_token, base_url):
    """Fixture create contact"""
    url = f"{base_url}/contacts"
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

    response = requests.post(url, json=body, headers=headers)
    data = response.json()
    contact_id = data["_id"]
    return contact_id
