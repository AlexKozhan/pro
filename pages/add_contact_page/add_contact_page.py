from playwright.sync_api import Page
import logging
from pages.add_contact_page.locators import FIRST_NAME, LAST_NAME, BIRTHDATE, EMAIL, PHONE, STREET1, STREET2, CITY, \
    STATE_PROVINCE, POSTAL_CODE, COUNTRY, SUBMIT_BUTTON, CANCEL_BUTTON, ERROR_MESSAGE


logger = logging.getLogger(__name__)


class AddContactPage:
    """Class Add Contact Page"""

    def __init__(self, page: Page):
        """Initializes an instance of the AddContactPage class."""
        self.page = page
        self.CONTACT_ROW = page.locator(
            "tr.contactTableBodyRow")

    def wait_for_contact_to_appear(self):
        """Ожидание появления контакта в списке"""
        self.CONTACT_ROW.wait_for(state="visible", timeout=10000)

    def enter_first_name(self, fn):
        """Enter first name"""
        logger.info(f"Entering first name: {fn} using selector: {FIRST_NAME}.")
        self.page.locator(FIRST_NAME).fill(fn)

    def enter_last_name(self, ln):
        """Enter last name"""
        logger.info(f"Entering last name: {ln} using selector: {LAST_NAME}.")
        self.page.locator(LAST_NAME).fill(ln)

    def enter_birthdate(self, bd):
        """Enter birthdate"""
        logger.info(f"Entering birthdate: {bd} using selector: {BIRTHDATE}.")
        self.page.locator(BIRTHDATE).fill(bd)

    def enter_email(self, eml1):
        """Enter email"""
        logger.info(f"Entering email: {eml1} using selector: {EMAIL}.")
        self.page.locator(EMAIL).fill(eml1)

    def enter_phone(self, pn):
        """Enter phone"""
        logger.info(f"Entering phone: {pn} using selector: {PHONE}.")
        self.page.locator(PHONE).fill(pn)

    def enter_street1(self, str1):
        """Enter street 1"""
        logger.info(f"Entering street1: {str1} using selector: {STREET1}.")
        self.page.locator(STREET1).fill(str1)

    def enter_street2(self, str2):
        """Enter street 2"""
        logger.info(f"Entering street2: {str2} using selector: {STREET2}.")
        self.page.locator(STREET2).fill(str2)

    def enter_city(self, ct):
        """Enter city"""
        logger.info(f"Entering city: {ct} using selector: {CITY}.")
        self.page.locator(CITY).fill(ct)

    def enter_state_province(self, stpr):
        """Enter state or province"""
        logger.info(f"Entering state/province: {stpr} using selector: {STATE_PROVINCE}.")
        self.page.locator(STATE_PROVINCE).fill(stpr)

    def enter_postal_code(self, pc):
        """Enter postal code"""
        logger.info(f"Entering postal code: {pc} using selector: {POSTAL_CODE}.")
        self.page.locator(POSTAL_CODE).fill(pc)

    def enter_country(self, cntr):
        """Enter country"""
        logger.info(f"Entering country: {cntr} using selector: {COUNTRY}.")
        self.page.locator(COUNTRY).fill(cntr)

    def click_submit_button(self):
        """Click submit button"""
        logger.info(f"Clicking submit button using selector: {SUBMIT_BUTTON}.")
        self.page.locator(SUBMIT_BUTTON).click()

    def click_cancel_button(self):
        """Click cancel button"""
        logger.info(f"Clicking cancel button using selector: {CANCEL_BUTTON}.")
        self.page.locator(CANCEL_BUTTON).click()

    def add_contact(self, fn, ln, bd, eml1, pn, str1, str2, ct, stpr, pc, cntr):
        """Add a contact by entering all details and clicking submit"""
        self.enter_first_name(fn)
        self.enter_last_name(ln)
        self.enter_birthdate(bd)
        self.enter_email(eml1)
        self.enter_phone(pn)
        self.enter_street1(str1)
        self.enter_street2(str2)
        self.enter_city(ct)
        self.enter_state_province(stpr)
        self.enter_postal_code(pc)
        self.enter_country(cntr)
        self.click_submit_button()

    def get_error_message(self, message):
        """Get error message"""
        if self.page.locator(ERROR_MESSAGE).is_visible():
            error_message = self.page.locator(ERROR_MESSAGE).text_content()
            if message in error_message:
                logger.info(f"Found error message: {error_message}")
                return error_message
        return None
