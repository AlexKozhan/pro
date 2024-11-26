from playwright.sync_api import Page
import logging
from pages.contact_list_page.locators import ADD_BUTTON, FIRST_ROW, LOGOUT_BUTTON, ROW_NAME, ROW_BIRTHDATE, ROW_EMAIL, \
    ROW_PHONE, ROW_ADDRESS, ROW_CITY, ROW_COUNTRY, CONTACT_LIST

# Логгер
logger = logging.getLogger(__name__)

class ContactListPage:
    """Class Contact List Page"""

    def __init__(self, page: Page):
        """Initializes an instance of the ContactListPage class."""
        self.page = page

    def click_add_button(self):
        """Click the 'Add' button."""
        logger.info(f"Clicking add button using selector: {ADD_BUTTON}.")
        add_button = self.page.locator(ADD_BUTTON)
        add_button.click()

    def click_first_row(self):
        """Click the first row."""
        logger.info(f"Clicking the first row using selector: {FIRST_ROW}.")
        first_row = self.page.locator(FIRST_ROW)
        first_row.click()

    def find_row(self):
        """Find the first row."""
        try:
            row = self.page.locator(FIRST_ROW)
            row.wait_for(state="visible", timeout=3000)  # Wait for the row to be visible
            return True
        except Exception as e:
            logger.error(f"Row not found: {str(e)}")
            return False

    def get_row_name(self):
        """Get the first row's name."""
        row_name_selector = f"{FIRST_ROW} {ROW_NAME}"
        row_name = self.page.locator(row_name_selector).text_content()
        logger.info(f"Row name: {row_name}")
        return row_name

    def get_row_birthdate(self):
        """Get the first row's birthdate."""
        row_birthdate_selector = f"{FIRST_ROW} {ROW_BIRTHDATE}"
        row_birthdate = self.page.locator(row_birthdate_selector).text_content()
        logger.info(f"Row birthdate: {row_birthdate}")
        return row_birthdate

    def get_row_email(self):
        """Get the first row's email."""
        row_email_selector = f"{FIRST_ROW} {ROW_EMAIL}"
        row_email = self.page.locator(row_email_selector).text_content()
        logger.info(f"Row email: {row_email}")
        return row_email

    def get_row_phone(self):
        """Get the first row's phone."""
        row_phone_selector = f"{FIRST_ROW} {ROW_PHONE}"
        row_phone = self.page.locator(row_phone_selector).text_content()
        logger.info(f"Row phone: {row_phone}")
        return row_phone

    def get_row_address(self):
        """Get the first row's address."""
        row_address_selector = f"{FIRST_ROW} {ROW_ADDRESS}"
        row_address = self.page.locator(row_address_selector).text_content()
        logger.info(f"Row address: {row_address}")
        return row_address

    def get_row_city(self):
        """Get the first row's city."""
        row_city_selector = f"{FIRST_ROW} {ROW_CITY}"
        row_city = self.page.locator(row_city_selector).text_content()
        logger.info(f"Row city: {row_city}")
        return row_city

    def get_row_country(self):
        """Get the first row's country."""
        row_country_selector = f"{FIRST_ROW} {ROW_COUNTRY}"
        row_country = self.page.locator(row_country_selector).text_content()
        logger.info(f"Row country: {row_country}")
        return row_country

    def get_all_row_data(self):
        """Get all data of the first row."""
        return [
            self.get_row_name(), self.get_row_birthdate(),
            self.get_row_email(), self.get_row_phone(), self.get_row_address(),
            self.get_row_city(), self.get_row_country()
        ]

    def click_logout_button(self):
        """Click logout button."""
        logger.info(f"Clicking logout button using selector: {LOGOUT_BUTTON}.")
        logout_button = self.page.locator(LOGOUT_BUTTON)
        logout_button.click()

    def is_contact_list_visible(self) -> bool:
        """Check if the contact list is visible."""
        try:
            contact_list = self.page.locator(CONTACT_LIST)  # Замените на локатор для списка контактов
            contact_list.wait_for(state="visible", timeout=5000)  # Ожидание появления списка контактов
            return True
        except Exception as e:
            logger.error(f"Contact list not visible: {str(e)}")
            return False

    def wait_for_contact_list_to_appear(self, timeout: int = 10000):  # Увеличьте таймаут
        """Wait for the contact list to appear on the page."""
        try:
            # Убедитесь, что страница полностью загрузилась
            self.page.wait_for_load_state("networkidle", timeout=15000)  # Увеличьте таймаут для загрузки страницы

            # Дождемся, пока элемент прикрепится к DOM
            contact_list = self.page.locator(".contacts")
            contact_list.wait_for(state="attached", timeout=timeout)  # Ждем, пока элемент будет прикреплен к DOM
            logger.info("Contact list is attached to DOM.")

            # Дождемся, пока элемент станет видимым
            contact_list.wait_for(state="visible", timeout=timeout)
            logger.info("Contact list is visible.")

        except Exception as e:
            logger.error(f"Contact list did not appear: {str(e)}")
            raise TimeoutError("Contact list did not appear within the specified timeout.")

    def wait_for_contact_to_disappear(self, timeout: int = 5000):
        """Wait for a contact to disappear from the list (after deletion)."""
        try:
            # Ожидаем, что контакт исчезнет
            first_row = self.page.locator(FIRST_ROW)
            first_row.wait_for(state="detached", timeout=timeout)  # Ожидаем исчезновения
            logger.info("Contact disappeared from the list.")
        except Exception as e:
            logger.error(f"Contact did not disappear: {str(e)}")
            raise TimeoutError("Contact did not disappear within the specified timeout.")
