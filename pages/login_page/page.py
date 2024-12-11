import allure
from playwright.sync_api import Page
from config import LOGIN_PAGE_URL
from pages.base_page import BasePage
from pages.login_page.locators import LoginPageLocators


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.USERNAME_INPUT = page.locator(LoginPageLocators.USERNAME_INPUT)
        self.PASSWORD_INPUT = page.locator(LoginPageLocators.PASSWORD_INPUT)
        self.LOGIN_BUTTON = page.locator("button#submit")
        self.ERROR_MESSAGE = page.locator("span#error")

    @allure.step("Entering username")
    def enter_username(self, username: str):
        self.USERNAME_INPUT.fill(username)

    @allure.step("Entering password")
    def enter_password(self, password: str):
        self.PASSWORD_INPUT.fill(password)

    @allure.step("Clicking login button")
    def click_login_button(self):
        self.LOGIN_BUTTON.click()

    @allure.step("Login to the system")
    def login(self, username, password):
        """Login to the system with given username and password."""
        if not LOGIN_PAGE_URL:
            raise ValueError("LOGIN_PAGE_URL is not defined or is empty!")

        self.page.goto(LOGIN_PAGE_URL)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    @allure.step("Checking if error message is visible")
    def is_error_message_visible(self) -> bool:
        """Check if error message appears (for invalid login attempts)."""
        try:
            self.ERROR_MESSAGE.wait_for(state="visible", timeout=10000)
            print("Error message is visible.")
            return True
        except Exception as e:
            print(f"Error message not visible: {e}")
            return False

    @allure.step("Checking if login button is visible")
    def is_login_button_visible(self) -> bool:
        """Check if login button is still visible (after logout)."""
        return self.LOGIN_BUTTON.is_visible()

    @allure.step("Verifying login page is loaded")
    def is_login_page_loaded(self) -> bool:
        """Check if the login page is loaded (checking the presence of the login button)."""
        return self.LOGIN_BUTTON.is_visible()

    @allure.step("Clicking the login button without credentials")
    def click_login_button_without_credentials(self):
        """Click the login button without entering credentials."""
        self.LOGIN_BUTTON.click()
