from playwright.sync_api import Page
import logging
from pages.base_page import BasePage
from pages.contact_details_page.locators import (
    EDIT_BUTTON, DELETE_BUTTON, RETURN_BUTTON,
    FIRST_NAME, LAST_NAME, \
    BIRTHDATE, EMAIL, PHONE, STREET1, STREET2,
    CITY, STATE_PROVINCE, POSTAL_CODE, COUNTRY)


logger = logging.getLogger(__name__)


class ContactDetailsPage(BasePage):
    """Class Contact Details Page"""

    def __init__(self, page: Page):
        """Initializes an instance of the
        ContactDetailsPage class."""
        super().__init__(page)
        self.page = page

    def click_edit_button(self):
        """Click the edit button"""
        logger.info(f"Clicking the edit button using "
                    f"locator: {EDIT_BUTTON}.")
        self.page.click(EDIT_BUTTON)

    def click_delete_button(self):
        """Click the delete button"""
        logger.info(f"Clicking the delete button using "
                    f"locator: {DELETE_BUTTON}.")
        self.page.click(DELETE_BUTTON)

    def click_return_button(self):
        """Click the return button"""
        logger.info(f"Clicking the return button using "
                    f"locator: {RETURN_BUTTON}.")
        self.page.click(RETURN_BUTTON)

    def get_first_name_text(self):
        """Get first name text"""
        logger.info(f"Getting first name text using "
                    f"locator: {FIRST_NAME}.")
        return self.page.locator(FIRST_NAME).text_content()

    def get_last_name_text(self):
        """Get last name text"""
        logger.info(f"Getting last name text using "
                    f"locator: {LAST_NAME}.")
        return self.page.locator(LAST_NAME).text_content()

    def get_birthdate_text(self):
        """Get birthdate text"""
        logger.info(f"Getting birthdate text using "
                    f"locator: {BIRTHDATE}.")
        return self.page.locator(BIRTHDATE).text_content()

    def get_email_text(self):
        """Get email text"""
        logger.info(f"Getting email text using "
                    f"locator: {EMAIL}.")
        return self.page.locator(EMAIL).text_content()

    def get_phone_text(self):
        """Get phone text"""
        logger.info(f"Getting phone text using "
                    f"locator: {PHONE}.")
        return self.page.locator(PHONE).text_content()

    def get_address1_text(self):
        """Get address1 text"""
        logger.info(f"Getting address1 text using "
                    f"locator: {STREET1}.")
        return self.page.locator(STREET1).text_content()

    def get_address2_text(self):
        """Get address2 text"""
        logger.info(f"Getting address2 text using "
                    f"locator: {STREET2}.")
        return self.page.locator(STREET2).text_content()

    def get_city_text(self):
        """Get city text"""
        logger.info(f"Getting city text using "
                    f"locator: {CITY}.")
        return self.page.locator(CITY).text_content()

    def get_state_province_text(self):
        """Get state/province text"""
        logger.info(f"Getting state/province text using "
                    f"locator: {STATE_PROVINCE}.")
        return self.page.locator(STATE_PROVINCE).text_content()

    def get_postal_code_text(self):
        """Get postal code text"""
        logger.info(f"Getting postal code text using "
                    f"locator: {POSTAL_CODE}.")
        return self.page.locator(POSTAL_CODE).text_content()

    def get_country_text(self):
        """Get country text"""
        logger.info(f"Getting country text using"
                    f" locator: {COUNTRY}.")
        return self.page.locator(COUNTRY).text_content()

    def get_all_contact_details_data(self):
        """Get all contact details data"""
        return [
            self.get_first_name_text(), self.get_last_name_text(),
            self.get_birthdate_text(), self.get_email_text(),
            self.get_phone_text(), self.get_address1_text(),
            self.get_address2_text(), self.get_city_text(),
            self.get_state_province_text(),
            self.get_postal_code_text(),
            self.get_country_text()
        ]

    def confirm_delete(self):
        try:
            logger.info(f"Page URL before confirmation: "
                        f"{self.page.url}")
            logger.info(f"HTML content before confirmation:"
                        f" {self.page.content()}")

            confirmation_popup = self.page.locator('text="Are '
                                                   'you sure you '
                                                   'want to delete '
                                                   'this contact?"')

            confirmation_popup.wait_for(state="visible",
                                        timeout=20000)

            delete_button = self.page.locator('button:'
                                              'has-text("Delete'
                                              ' Contact")')
            delete_button.wait_for(state="visible", timeout=20000)


            delete_button.click()

            logger.info("Contact deletion confirmed")
        except TimeoutError:
            logger.error("Modal did not appear in time")
            self.page.screenshot(path="timeout_error.png")
            raise

    def cancel_delete(self):
        """Handle the cancel action on delete confirmation popup"""
        try:
            (self.page.locator('text="Are you sure you want '
                              'to delete this contact?"').
             wait_for(state="visible", timeout=5000))
            logger.info("Delete confirmation popup appeared.")

            self.page.locator('button:has-text("Отмена")').click()
            logger.info("Clicked 'Отмена' on delete "
                        "confirmation popup.")

        except Exception as e:
            logger.error(f"Delete confirmation popup not found: {str(e)}")
            raise TimeoutError("Delete confirmation popup did "
                               "not appear within the specified timeout.")
