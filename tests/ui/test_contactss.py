"""Tests with Playwright"""
import pytest
import allure
from pages.login_page.page import LoginPage
from pages.contact_list_page.Contact_List_Page import ContactListPage
from pages.add_contact_page.add_contact_page import AddContactPage
from pages.contact_details_page.contact_details_page import ContactDetailsPage
from pages.edit_contact_page.edit_contact_page import EditContactPage
from Test_data import test_data
from logger import logger


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.critical
@pytest.mark.UI
def test_add_contact(page):
    """Test add contact successfully"""
    # Navigate to the contact list page if necessary
    page.goto("https://thinking-tester-contact-list.herokuapp.com/contactList")

    assert test_data.url1 in page.url
    clp = ContactListPage(page)
    clp.click_add_button()
    clp.wait_url_contains(test_data.url_contain2)
    assert test_data.url2 in page.url

    acp = AddContactPage(page)
    acp.add_contact(test_data.fn, test_data.ln, test_data.bd,
                    test_data.eml1, test_data.pn, test_data.str1,
                    test_data.str2, test_data.ct, test_data.stpr,
                    test_data.pc, test_data.cntr)
    clp.wait_url_contains(test_data.url_contain1)
    actual_result = clp.get_all_row_data()
    expected_result = [
        f"{test_data.fn} {test_data.ln}", test_data.bd, test_data.eml1,
        test_data.pn, f"{test_data.str1} {test_data.str2}",
        f"{test_data.ct} {test_data.stpr} {test_data.pc}", test_data.cntr]
    assert actual_result == expected_result
    clp.click_first_row()
    clp.wait_url_contains(test_data.url_contain3)
    assert test_data.url3 in page.url
    cdp = ContactDetailsPage(page)
    cdp.click_delete_button()
    page.on("dialog", lambda dialog: dialog.accept())
    cdp.wait_url_contains(test_data.url_contain1)
    assert clp.find_row() is False
    logger.info("Test add contact successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_cancel_add_contact(page):
    """Test cancel add contact successfully"""
    clp = ContactListPage(page)
    clp.click_add_button()
    clp.wait_url_contains(test_data.url_contain2)
    assert test_data.url2 in page.url

    acp = AddContactPage(page)
    acp.click_cancel_button()
    assert test_data.url1 in page.url
    logger.info("Test cancel add contact successfully complete")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_edit_contact(page, created_contact):
    """Test edit contact successfully"""
    clp = ContactListPage(page)
    clp.click_first_row()

    cdp = ContactDetailsPage(page)
    cdp.click_edit_button()
    cdp.wait_url_contains(test_data.url_contain4)
    ecp = EditContactPage(page)
    ecp.wait_for_value_in_element("input[name='firstName']", test_data.fn)
    ecp.edit_contact(test_data.fn_1, test_data.ln_1, test_data.bd_1,
                     test_data.eml1_1, test_data.pn_1, test_data.str1_1,
                     test_data.str2_1, test_data.ct_1, test_data.stpr_1,
                     test_data.pc_1, test_data.cntr_1)
    ecp.wait_for_value_in_element("input[name='firstName']", test_data.fn_1)
    expected_result = [
        test_data.fn_1, test_data.ln_1, test_data.bd_1,
        test_data.eml1_1, test_data.pn_1, test_data.str1_1,
        test_data.str2_1, test_data.ct_1, test_data.stpr_1,
        test_data.pc_1, test_data.cntr_1
    ]
    actual_result = cdp.get_all_contact_details_data()
    assert actual_result == expected_result
    cdp.click_return_button()
    logger.info("Test edit contact successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_cancel_edit_contact(page, created_contact):
    """Test cancel edit contact successfully"""
    clp = ContactListPage(page)
    clp.click_first_row()

    cdp = ContactDetailsPage(page)
    cdp.click_edit_button()
    cdp.wait_url_contains(test_data.url_contain4)
    ecp = EditContactPage(page)
    ecp.wait_for_value_in_element("input[name='firstName']", test_data.fn)
    ecp.click_cancel_button()
    ecp.wait_for_value_in_element("input[name='firstName']", test_data.fn)
    expected_result = [
        test_data.fn, test_data.ln, test_data.bd,
        test_data.eml1, test_data.pn, test_data.str1,
        test_data.str2, test_data.ct, test_data.stpr,
        test_data.pc, test_data.cntr
    ]
    actual_result = cdp.get_all_contact_details_data()
    assert actual_result == expected_result
    cdp.click_return_button()
    logger.info("Test cancel edit contact successfully complete")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_delete_contact(page, created_contact):
    """Test delete contact successfully"""
    lp = LoginPage(page)
    lp.login(test_data.eml, test_data.psw)
    assert test_data.url1 in page.url

    clp = ContactListPage(page)
    clp.click_add_button()
    clp.wait_url_contains(test_data.url_contain2)
    assert test_data.url2 in page.url

    acp = AddContactPage(page)
    acp.add_contact(test_data.fn, test_data.ln, test_data.bd,
                    test_data.eml1, test_data.pn, test_data.str1,
                    test_data.str2, test_data.ct, test_data.stpr,
                    test_data.pc, test_data.cntr)
    clp.wait_url_contains(test_data.url_contain1)
    clp.click_first_row()
    clp.wait_url_contains(test_data.url_contain3)
    assert test_data.url3 in page.url
    cdp = ContactDetailsPage(page)
    cdp.click_delete_button()
    page.on("dialog", lambda dialog: dialog.accept())
    cdp.wait_url_contains(test_data.url_contain1)
    assert clp.find_row() is False
    logger.info("Test delete contact successfully complete")
