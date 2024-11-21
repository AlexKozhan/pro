"""Conftest module"""
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from UI.Pages.add_contact_page import AddContactPage
from UI.Pages.contact_details_page import ContactDetailsPage
from UI.Pages.contact_list_page import ContactListPage
from UI.Pages.login_page import LoginPage
from UI.Test_data import test_data


@pytest.fixture
def driver():
    """Fixture for initializing and quitting a Chrome WebDriver instance
     in headless mode"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome = webdriver.Chrome(options=chrome_options)
    chrome.implicitly_wait(5)
    chrome.get(test_data.url)
    yield chrome
    chrome.quit()


@pytest.fixture
def login_user(driver):
    """Login as user."""
    lp = LoginPage(driver)
    lp.complete_login(test_data.eml, test_data.psw)
    lp.wait_url(driver, test_data.url_contain1)


@pytest.fixture
def created_contact(driver, login_user):
    """Create new contact."""
    clp = ContactListPage(driver)
    clp.click_add_button()
    clp.wait_url(driver, test_data.url_contain2)

    acp = AddContactPage(driver)
    acp.add_contact(test_data.fn, test_data.ln, test_data.bd,
                    test_data.eml1, test_data.pn, test_data.str1,
                    test_data.str2, test_data.ct, test_data.stpr,
                    test_data.pc, test_data.cntr)
    acp.wait_url(driver, test_data.url_contain1)
    yield acp
    clp.click_first_row()
    cdp = ContactDetailsPage(driver)
    cdp.click_delete_button()
    alert = driver.switch_to.alert
    alert.accept()
    cdp.wait_url(driver, test_data.url_contain1)
    clp = ContactListPage(driver)


@pytest.fixture(scope="session")
def unique_email():
    """Fixture to generate a unique email"""
    return f"{uuid.uuid4()}@example.com"


@pytest.fixture(scope="session")
def existing_email():
    """Fixture to provide an existing email for testing"""
    return "john.doe112111@example.com"
