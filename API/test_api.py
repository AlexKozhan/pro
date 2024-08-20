"""
API tests to check the functionality of the contact list.
"""
import requests
import allure
from API.random_data import generate_email, generate_string
from API import test_data


@allure.severity(allure.severity_level.NORMAL)
def test_delete_user_unauthorized(base_url):
    """TC013: Delete User - 401 Unauthorized "Please
    authenticate."""
    url = f"{base_url}/users/me"
    headers = {}

    response = requests.delete(url, headers=headers)

    assert response.status_code == 401
    assert response.json().get("error") == ("Please "
                                            "authenticate.")


@allure.severity(allure.severity_level.CRITICAL)
def test_add_contact_success(auth_token, base_url, cleanup_contacts):
    """TC014: Add Contact - 201 Created"""
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

    assert response.status_code == 201
    data = response.json()
    assert data["firstName"] == "John"
    assert data["lastName"] == "Doe"
    assert data["owner"] is not None


@allure.severity(allure.severity_level.NORMAL)
def test_add_contact_unauthorized(base_url):
    """TC015: Add Contact - 401 Unauthorized "Please
    authenticate."""
    url = f"{base_url}/contacts"
    headers = {}
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

    assert response.status_code == 401
    assert response.json().get("error") == ("Please "
                                            "authenticate.")


@allure.severity(allure.severity_level.MINOR)
def test_add_contact_bad_request(auth_token, base_url, cleanup_contacts):
    """TC016: Add Contact - 400 Bad Request"""
    url = f"{base_url}/contacts"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    body = {}

    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 400

    response_json = response.json()

    assert "errors" in response_json
    assert "_message" in response_json
    assert "message" in response_json

    assert "firstName" in response_json["errors"]
    assert "lastName" in response_json["errors"]

    assert (response_json["errors"]["firstName"]["message"] ==
            "Path `firstName` is required.")
    assert (response_json["errors"]["lastName"]["message"] ==
            "Path `lastName` is required.")


@allure.severity(allure.severity_level.CRITICAL)
def test_get_contact_list_success(auth_token, base_url, cleanup_contacts):
    """TC017: Get Contact List - 200 OK"""
    url = f"{base_url}/contacts"
    headers = {
        "Authorization": f"Bearer {auth_token}",
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        contact = data[0]
        assert "firstName" in contact
        assert "lastName" in contact


@allure.severity(allure.severity_level.NORMAL)
def test_get_contact_list_unauthorized(base_url):
    """TC018: Get Contact List - 401 Unauthorized
    "Please authenticate."""
    url = f"{base_url}/contacts"
    headers = {}

    response = requests.get(url, headers=headers)

    assert response.status_code == 401
    assert response.json().get("error") == ("Please "
                                            "authenticate.")


@allure.severity(allure.severity_level.CRITICAL)
def test_register_user_success(base_url):
    """TC001: Register User - 200 OK"""
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
    assert response.status_code == 201
    assert response.json().keys() == {"user", "token"}
    assert response.json().get("user").get("firstName") == first_name
    assert response.json().get("user").get("lastName") == last_name
    assert response.json().get("user").get("email") == email.lower()


@allure.severity(allure.severity_level.NORMAL)
def test_add_user_email_already_in_use(base_url, register_user):
    """TC002: Add User - 400  Bad request 'Email address is already
     in use'"""
    url = f"{base_url}/users"
    first_name = generate_string(3, 6)
    last_name = generate_string(5, 10)
    body = {
        "firstName": first_name,
        "lastName": last_name,
        "email": test_data.u_email,
        "password": "Tester11"
    }
    response = requests.post(url, json=body)
    assert response.status_code == 400
    assert response.json().get("message") == ("Email address is"
                                              " already in use")


@allure.severity(allure.severity_level.MINOR)
def test_add_user_incorrect_body(base_url):
    """TC003: Add User - 400 Bad request "User validation
     failed" (Empty body)"""
    url = f"{base_url}/users"
    incorrect_body = {}
    response = requests.post(url, json=incorrect_body)
    assert response.status_code == 400
    assert response.json().keys() == {"errors", "_message", "message"}
    assert response.json().get("message") == ("User validation failed: "
                                              "password: Path `password` is"
                                              " required., lastName: Path "
                                              "`lastName` is required., "
                                              "firstName: Path `firstName` "
                                              "is required.")


@allure.severity(allure.severity_level.CRITICAL)
def test_get_user_profile_success(auth_token, base_url):
    """TC004: Get User Profile - 200 Ok"""
    url = f"{base_url}/users/me"
    headers = {
        "Authorization": f"Bearer {auth_token}",
    }

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json().keys() == {"_id", "firstName", "lastName",
                                      "email", "__v"}
    assert response.json().get("_id") == test_data.id_user_from_auth_token


@allure.severity(allure.severity_level.NORMAL)
def test_get_user_profile_unauthorized(base_url):
    """TC005: Get User Profile - 401 Unauthorized "Please authenticate."""
    url = f"{base_url}/users/me"
    headers = {}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    assert response.json().get("error") == "Please authenticate."


@allure.severity(allure.severity_level.CRITICAL)
def test_update_user_success(user_with_token, base_url):
    """TC006: Update User - 200 Ok"""
    url = f"{base_url}/users/me"
    headers = {
        "Authorization": f"Bearer {user_with_token['token']}",
    }
    first_name = generate_string(3, 6)
    last_name = generate_string(5, 10)
    email = generate_email()
    body = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": "myNewPassword"
    }
    response = requests.patch(url, headers=headers, json=body)
    assert response.status_code == 200
    assert response.json().get("firstName") == first_name
    assert response.json().get("lastName") == last_name
    assert response.json().get("email") == email.lower()


@allure.severity(allure.severity_level.CRITICAL)
def test_update_contact_success(auth_token, base_url,
                                created_contact, cleanup_contacts):
    """TC019: Successful update contact
     via correct test data and using PUT method"""
    url = f"{base_url}/contacts/{created_contact}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    body = {
        "firstName": "Amy",
        "lastName": "Miller",
        "birthdate": "1992-02-02",
        "email": "amiller@fake.com",
        "phone": "8005554242",
        "street1": "13 School St.",
        "street2": "Apt. 5",
        "city": "Washington",
        "stateProvince": "QC",
        "postalCode": "A1A1A1",
        "country": "Canada"
    }

    response = requests.put(url, json=body, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == "Amy"
    assert data["lastName"] == "Miller"
    assert data["owner"] is not None


@allure.severity(allure.severity_level.MINOR)
def test_update_contact_bad_request_put_method(auth_token, base_url,
                                               created_contact,
                                               cleanup_contacts):
    """TC020: Unsuccessful update contact
     via empty body and using PUT method"""
    url = f"{base_url}/contacts/{created_contact}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    body = {}

    response = requests.put(url, json=body, headers=headers)
    assert response.status_code == 400

    response_json = response.json()

    assert "errors" in response_json
    assert "message" in response_json

    assert "firstName" in response_json["errors"]
    assert "lastName" in response_json["errors"]

    assert (response_json["errors"]["firstName"]["message"] ==
            "Path `firstName` is required.")
    assert (response_json["errors"]["lastName"]["message"] ==
            "Path `lastName` is required.")


@allure.severity(allure.severity_level.NORMAL)
def test_update_contact_unauthorized_put_method(base_url, created_contact,
                                                cleanup_contacts):
    """TC021: Unsuccessful update contact
     without auth token and using PUT method"""
    url = f"{base_url}/contacts/{created_contact}"
    headers = {"Content-Type": "application/json"}

    body = {
        "firstName": "Amy",
        "lastName": "Miller",
        "birthdate": "1992-02-02",
        "email": "amiller@fake.com",
        "phone": "8005554242",
        "street1": "13 School St.",
        "street2": "Apt. 5",
        "city": "Washington",
        "stateProvince": "QC",
        "postalCode": "A1A1A1",
        "country": "Canada"
    }

    response = requests.put(url, json=body, headers=headers)

    assert response.status_code == 401
    assert response.json().get("error") == ("Please "
                                            "authenticate.")


@allure.severity(allure.severity_level.CRITICAL)
def test_update_contact_success_firstname(auth_token, base_url,
                                          created_contact, cleanup_contacts):
    """TC022:Successful update contact first name using PATCH method"""
    url = f"{base_url}/contacts/{created_contact}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    body = {
        "firstName": "Anna",
    }

    response = requests.patch(url, json=body, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == "Anna"
    assert data["owner"] is not None


@allure.severity(allure.severity_level.MINOR)
def test_update_contact_success_patch_method(auth_token, base_url,
                                             created_contact,
                                             cleanup_contacts):
    """TC023: Successful update contact via empty body using PATCH method"""
    url = f"{base_url}/contacts/{created_contact}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    body = {}

    response = requests.patch(url, json=body, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["firstName"] == "John"
    assert data["lastName"] == "Doe"
    assert data["owner"] is not None


@allure.severity(allure.severity_level.NORMAL)
def test_update_contact_unauthorized_patch_method(base_url,
                                                  created_contact,
                                                  cleanup_contacts):
    """TC024: Unsuccessful update contact
     without auth token and using PATCH method"""
    url = f"{base_url}/contacts/{created_contact}"
    headers = {"Content-Type": "application/json"}

    body = {
        "firstName": "Anna",
    }

    response = requests.patch(url, json=body, headers=headers)

    assert response.status_code == 401
    assert response.json().get("error") == ("Please "
                                            "authenticate.")


@allure.severity(allure.severity_level.CRITICAL)
def test_delete_contact_success(auth_token, base_url, created_contact):
    """TC025: Successful delete contact with correct data"""
    url = f"{base_url}/contacts/{created_contact}"
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

    response = requests.get(url, headers=headers)
    assert response.status_code == 404


@allure.severity(allure.severity_level.NORMAL)
def test_delete_contact_unauthorized(base_url, created_contact,
                                     cleanup_contacts):
    """TC026: Unsuccessful delete contact without auth token"""
    url = f"{base_url}/contacts/{created_contact}"

    response = requests.delete(url)

    assert response.status_code == 401
    assert response.json().get("error") == ("Please "
                                            "authenticate.")