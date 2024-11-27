import allure
import pytest
from pages.login_page.page import LoginPage
from pages.contact_list_page.Contact_List_Page import ContactListPage
from config import USERNAME, PASSWORD
from pages.main_page.page import MainPage
from pages.add_contact_page.add_contact_page import AddContactPage
from pages.contact_details_page.contact_details_page import ContactDetailsPage
from logger import logger
from playwright.sync_api import Page

import pytest
import allure
from pages.SignUpPage.SignUpPage import SignUpPage
import logging
from pages.SignUpPage.locators import ERROR_ELEMENT

logger = logging.getLogger(__name__)


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.critical
@pytest.mark.UI
def test_successful_sign_up(page, unique_email):
    """TC006: Check successful sign up for user with valid data"""
    page.goto("https://thinking-tester-contact-list.herokuapp.com/addUser")
    sp = SignUpPage(page)
    sp.enter_data("John", "Doe", unique_email, "Password123!")

    assert sp.is_signup_successful(), "User was not successfully signed up"
    logger.info("Test successful sign up successfully complete")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_invalid_data_sign_up(page):
    """TC007: Check sign up for user with invalid data"""
    page.goto("https://thinking-tester-contact-list.herokuapp.com/addUser")
    sp = SignUpPage(page)
    sp.enter_data("John", "Doe", "invalid-email", "w1")

    # Log the current URL and page content for debugging
    logger.info(f"Current URL: {page.url}")
    logger.info("Page content before waiting for error message:")
    logger.info(page.content())


    # Increase the timeout and wait for the error message
    page.wait_for_selector(ERROR_ELEMENT, timeout=10000)

    error_message = sp.get_error_message()
    print(f"Retrieved error message: {error_message}")
    expected_error = (
        "User validation failed: email: Email is invalid, "
        "password: Path `password` (`w1`) is shorter than the minimum allowed length (7)."
    )
    assert error_message == expected_error, "No error message for invalid email"


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_existing_email_sign_up(page, existing_email):
    """TC008: Check sign up for user with an existing email"""
    page.goto("https://thinking-tester-contact-list.herokuapp.com/addUser")
    sp = SignUpPage(page)
    sp.enter_data("Jack", "Vorobei", existing_email, "Password123!")

    # Log the current URL and page content for debugging
    logger.info(f"Current URL: {page.url}")
    logger.info("Page content before retrieving error message:")
    logger.info(page.content())

    # Wait for the error message to appear
    try:
        page.wait_for_selector(ERROR_ELEMENT, timeout=10000)
    except Exception as e:
        logger.error(f"Error waiting for selector: {e}")
        logger.info("Page content after timeout:")
        logger.info(page.content())
        raise

    error_message = sp.get_error_message()
    logger.info(f"Retrieved error message: {error_message}")
    assert error_message == "Email address is already in use", "No error message for existing email"
    logger.info("Test sign up with existing email successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.smoke
@pytest.mark.UI
def test_empty_fields_sign_up(page):
    """TC009: Check sign up for user with empty fields"""
    page.goto("https://thinking-tester-contact-list.herokuapp.com/addUser")
    sp = SignUpPage(page)
    sp.click_add_user()
    page.wait_for_selector(ERROR_ELEMENT, timeout=10000)

    error_message = sp.get_error_message()
    expected_error = (
        "User validation failed: firstName: Path `firstName` is required., "
        "lastName: Path `lastName` is required., email: Email is invalid, "
        "password: Path `password` is required."
    )
    assert error_message == expected_error, "No error message for empty fields"
    logger.info("Test sign up with empty fields successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_cancel_sign_up(page):
    """TC010: Check cancellation of sign-up process"""
    page.goto("https://thinking-tester-contact-list.herokuapp.com/addUser")
    sp = SignUpPage(page)
    sp.enter_data("Temp", "User", "temp.user@example.com", "TempPass123!")
    sp.click_cancel()

    assert page.url == "https://thinking-tester-contact-list.herokuapp.com/login", \
        "User was not redirected to the home page after cancel"
    logger.info("Test cancel sign up successfully complete")