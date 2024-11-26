# edit_contact_page/edit_contact_page.py

from playwright.sync_api import Page
from pages.edit_contact_page.locators import FIRST_NAME, LAST_NAME, BIRTHDATE, EMAIL, PHONE, STREET1, STREET2, CITY, STATE_PROVINCE, POSTAL_CODE, COUNTRY, SUBMIT_BUTTON, CANCEL_BUTTON
import logging

# Логгер
logger = logging.getLogger(__name__)

class EditContactPage:
    """Class for editing contact page"""

    def __init__(self, page: Page):
        """Initializes an instance of the EditContactPage class."""
        self.page = page

    def edit_first_name(self, fn_1: str):
        """Edit first name"""
        logger.info(f"Editing first name to: {fn_1}")
        el_input = self.page.locator(FIRST_NAME)
        el_input.fill(fn_1)

    def edit_last_name(self, ln_1: str):
        """Edit last name"""
        logger.info(f"Editing last name to: {ln_1}")
        el_input = self.page.locator(LAST_NAME)
        el_input.fill(ln_1)

    def edit_birthdate(self, bd_1: str):
        """Edit birthdate"""
        logger.info(f"Editing birthdate to: {bd_1}")
        el_input = self.page.locator(BIRTHDATE)
        el_input.fill(bd_1)

    def edit_email(self, eml1_1: str):
        """Edit email"""
        logger.info(f"Editing email to: {eml1_1}")
        el_input = self.page.locator(EMAIL)
        el_input.fill(eml1_1)

    def edit_phone(self, pn_1: str):
        """Edit phone"""
        logger.info(f"Editing phone to: {pn_1}")
        el_input = self.page.locator(PHONE)
        el_input.fill(pn_1)

    def edit_street1(self, str1_1: str):
        """Edit street 1"""
        logger.info(f"Editing street 1 to: {str1_1}")
        el_input = self.page.locator(STREET1)
        el_input.fill(str1_1)

    def edit_street2(self, str2_1: str):
        """Edit street 2"""
        logger.info(f"Editing street 2 to: {str2_1}")
        el_input = self.page.locator(STREET2)
        el_input.fill(str2_1)

    def edit_city(self, ct_1: str):
        """Edit city"""
        logger.info(f"Editing city to: {ct_1}")
        el_input = self.page.locator(CITY)
        el_input.fill(ct_1)

    def edit_state_province(self, stpr_1: str):
        """Edit state or province"""
        logger.info(f"Editing state/province to: {stpr_1}")
        el_input = self.page.locator(STATE_PROVINCE)
        el_input.fill(stpr_1)

    def edit_postal_code(self, pc_1: str):
        """Edit postal code"""
        logger.info(f"Editing postal code to: {pc_1}")
        el_input = self.page.locator(POSTAL_CODE)
        el_input.fill(pc_1)

    def edit_country(self, cntr_1: str):
        """Edit country"""
        logger.info(f"Editing country to: {cntr_1}")
        el_input = self.page.locator(COUNTRY)
        el_input.fill(cntr_1)

    def click_submit_button(self):
        """Click submit button"""
        logger.info(f"Clicking submit button.")
        btn = self.page.locator(SUBMIT_BUTTON)
        btn.click()

    def click_cancel_button(self):
        """Click cancel button"""
        logger.info(f"Clicking cancel button.")
        btn = self.page.locator(CANCEL_BUTTON)
        btn.click()

    def edit_contact(self, fn_1: str, ln_1: str, bd_1: str, eml1_1: str, pn_1: str, str1_1: str,
                     str2_1: str, ct_1: str, stpr_1: str, pc_1: str, cntr_1: str):
        """Edit contact"""
        self.edit_first_name(fn_1)
        self.edit_last_name(ln_1)
        self.edit_birthdate(bd_1)
        self.edit_email(eml1_1)
        self.edit_phone(pn_1)
        self.edit_street1(str1_1)
        self.edit_street2(str2_1)
        self.edit_city(ct_1)
        self.edit_state_province(stpr_1)
        self.edit_postal_code(pc_1)
        self.edit_country(cntr_1)
        self.click_submit_button()
