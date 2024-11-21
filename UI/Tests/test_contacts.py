"""Tests"""
import pytest
import allure
from UI.Pages.login_page import LoginPage
from UI.Pages.contact_list_page import ContactListPage
from UI.Pages.add_contact_page import AddContactPage, first_name
from UI.Pages.contact_details_page import ContactDetailsPage
from UI.Pages.edit_contact_page import EditContactPage
from UI.Test_data import test_data
from logger import logger


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.critical
@pytest.mark.UI
def test_add_contact(driver, login_user):
    """Test add contact successfully"""
    assert test_data.url1 in driver.current_url
    clp = ContactListPage(driver)
    clp.click_add_button()
    clp.wait_url(driver, test_data.url_contain2)
    assert test_data.url2 in driver.current_url

    acp = AddContactPage(driver)
    acp.add_contact(test_data.fn, test_data.ln, test_data.bd,
                    test_data.eml1, test_data.pn, test_data.str1,
                    test_data.str2, test_data.ct, test_data.stpr,
                    test_data.pc, test_data.cntr)
    acp.wait_url(driver, test_data.url_contain1)
    actual_result = clp.get_all_row_data()
    expected_result = [
        f"{test_data.fn} {test_data.ln}", test_data.bd, test_data.eml1,
        test_data.pn, f"{test_data.str1} {test_data.str2}",
        f"{test_data.ct} {test_data.stpr} {test_data.pc}", test_data.cntr]
    assert actual_result == expected_result
    clp.click_first_row()
    clp.wait_url(driver, test_data.url_contain3)
    assert test_data.url3 in driver.current_url
    cdp = ContactDetailsPage(driver)
    cdp.click_delete_button()
    alert = driver.switch_to.alert
    alert.accept()
    cdp.wait_url(driver, test_data.url_contain1)
    clp = ContactListPage(driver)
    assert clp.find_row() is False
    logger.info("Test add contact successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_cancel_add_contact(driver, login_user):
    """Test cancel add contact successfully"""

    clp = ContactListPage(driver)
    clp.click_add_button()
    clp.wait_url(driver, test_data.url_contain2)
    assert test_data.url2 in driver.current_url

    acp = AddContactPage(driver)
    acp.click_cancel_button()
    assert test_data.url1 in driver.current_url
    logger.info("Test cancel add contact successfully complete")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_edit_contact(driver, login_user, created_contact):
    """Test edit contact successfully"""
    clp = ContactListPage(driver)
    clp.click_first_row()

    cdp = ContactDetailsPage(driver)
    cdp.click_edit_button()
    cdp.wait_url(driver, test_data.url_contain4)
    ecp = EditContactPage(driver)
    ecp.wait_value_in_element_appears(first_name, test_data.fn)
    ecp.edit_contact(test_data.fn_1, test_data.ln_1, test_data.bd_1,
                     test_data.eml1_1, test_data.pn_1, test_data.str1_1,
                     test_data.str2_1, test_data.ct_1, test_data.stpr_1,
                     test_data.pc_1, test_data.cntr_1)
    ecp.wait_value_in_element_appears(first_name, test_data.fn_1)
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
def test_cancel_edit_contact(driver, login_user, created_contact):
    """Test cancel edit contact successfully"""

    clp = ContactListPage(driver)
    clp.click_first_row()

    cdp = ContactDetailsPage(driver)
    cdp.click_edit_button()
    cdp.wait_url(driver, test_data.url_contain4)
    ecp = EditContactPage(driver)
    ecp.wait_value_in_element_appears(first_name, test_data.fn)
    ecp.click_cancel_button()
    ecp.wait_value_in_element_appears(first_name, test_data.fn)
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
def test_delete_contact(driver):
    """Test delete contact successfully"""
    lp = LoginPage(driver)
    lp.complete_login(test_data.eml, test_data.psw)
    lp.wait_url(driver, test_data.url_contain1)
    assert test_data.url1 in driver.current_url

    clp = ContactListPage(driver)
    clp.click_add_button()
    clp.wait_url(driver, test_data.url_contain2)
    assert test_data.url2 in driver.current_url

    acp = AddContactPage(driver)
    acp.add_contact(test_data.fn, test_data.ln, test_data.bd,
                    test_data.eml1, test_data.pn, test_data.str1,
                    test_data.str2, test_data.ct, test_data.stpr,
                    test_data.pc, test_data.cntr)
    acp.wait_url(driver, test_data.url_contain1)
    clp.click_first_row()
    clp.wait_url(driver, test_data.url_contain3)
    assert test_data.url3 in driver.current_url
    cdp = ContactDetailsPage(driver)
    cdp.click_delete_button()
    alert = driver.switch_to.alert
    alert.accept()
    cdp.wait_url(driver, test_data.url_contain1)
    clp = ContactListPage(driver)
    assert clp.find_row() is False
    logger.info("Test delete contact successfully complete")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.critical
@pytest.mark.UI
def test_view_contact(driver, created_contact):
    """Test view contact successfully"""
    clp = ContactListPage(driver)
    actual_result = clp.get_all_row_data()
    expected_result = [
        f"{test_data.fn} {test_data.ln}", test_data.bd, test_data.eml,
        test_data.pn, f"{test_data.str1} {test_data.str2}",
        f"{test_data.ct} {test_data.stpr} {test_data.pc}", test_data.cntr]
    assert actual_result == expected_result
    logger.info("Test view contact successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_view_empty_contact(driver, login_user):
    """Test view empty list contact successfully"""
    clp = ContactListPage(driver)
    assert clp.find_row() is False
    logger.info("Test view empty contact successfully complete")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_add_contact_with_inv_data(driver, login_user):
    """Test add contact with invalid data unsuccessfully"""
    clp = ContactListPage(driver)
    clp.click_add_button()
    clp.wait_url(driver, test_data.url_contain2)
    assert test_data.url2 in driver.current_url

    acp = AddContactPage(driver)
    acp.add_contact(test_data.fn, test_data.ln, test_data.inv_bd,
                    test_data.inv_eml, test_data.inv_pn, test_data.str1,
                    test_data.str2, test_data.ct, test_data.stpr,
                    test_data.inv_pc, test_data.cntr)
    assert (acp.get_error_message(test_data.error_message_add_new_contact)
            == test_data.error_message_add_new_contact)
    logger.info("Test add contact with invalid data successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.smoke
@pytest.mark.UI
def test_add_contact_with_empty_data(driver, login_user):
    """Test add contact with empty data unsuccessfully"""
    clp = ContactListPage(driver)
    clp.click_add_button()
    clp.wait_url(driver, test_data.url_contain2)
    assert test_data.url2 in driver.current_url

    acp = AddContactPage(driver)
    acp.add_contact("", "", test_data.bd,
                    test_data.eml, test_data.pn, test_data.str1,
                    test_data.str2, test_data.ct, test_data.stpr,
                    test_data.pc, test_data.cntr)
    assert (acp.get_error_message(
            test_data.error_message_empty_add_new_contact) ==
            test_data.error_message_empty_add_new_contact)
    logger.info("Test add contact with empty data successfully complete")
