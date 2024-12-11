# sign_up_page/sign_up_page.py

from playwright.sync_api import Page
from pages.SignUpPage.locators import FIRST_NAME, LAST_NAME, EMAIL, PASSWORD, ADD_USER_BUTTON, CANCEL_BUTTON, ERROR_ELEMENT
import logging

# Логгер
logger = logging.getLogger(__name__)

class SignUpPage:
    """Class for interacting with the sign-up page"""

    def __init__(self, page: Page):
        """Initializes an instance of the SignUpPage"""
        self.page = page

    def enter_first_name(self, name: str):
        """Enter first name"""
        logger.info(f"Entering first name: {name}")
        el_input = self.page.locator(FIRST_NAME)
        el_input.fill(name)

    def enter_last_name(self, name: str):
        """Enter last name"""
        logger.info(f"Entering last name: {name}")
        el_input = self.page.locator(LAST_NAME)
        el_input.fill(name)

    def enter_email(self, email: str):
        """Enter email"""
        logger.info(f"Entering email: {email}")
        el_input = self.page.locator(EMAIL)
        el_input.fill(email)

    def enter_password(self, password: str):
        """Enter password"""
        logger.info(f"Entering password: {password}")
        el_input = self.page.locator(PASSWORD)
        el_input.fill(password)

    def click_add_user(self):
        """Click on the add user button"""
        logger.info(f"Clicking add user button.")
        btn = self.page.locator(ADD_USER_BUTTON)
        btn.click()

    def click_cancel(self):
        """Click on the cancel button"""
        logger.info(f"Clicking cancel button.")
        btn = self.page.locator(CANCEL_BUTTON)
        btn.click()

    def get_error_message(self) -> str:
        """Retrieve the error message displayed on the sign-up page"""
        try:
            error_element = self.page.locator(ERROR_ELEMENT)
            return error_element.text_content()
        except:
            return ""

    def is_signup_successful(self) -> bool:
        """Check if signup was successful by looking for a specific element on the homepage"""
        try:
            # Можно использовать проверку URL или наличие конкретного элемента
            self.page.wait_for_url("**/contactList")
            return True
        except:
            return False

    def enter_data(self, first_name: str, last_name: str, email: str, password: str):
        """Enter signup data"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password(password)
        self.click_add_user()
