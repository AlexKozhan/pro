"""Authorization tests"""

import pytest
import allure
from UI.Pages.login_page import LoginPage, error, email, password
from UI.Pages.contact_list_page import ContactListPage
from UI.Test_data import test_data
from logger import logger


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_login_success(driver):
    """Test login successfully"""
    lp = LoginPage(driver)
    lp.complete_login(test_data.eml, test_data.psw)
    clp = ContactListPage(driver)
    clp.wait_url(driver, test_data.url_contain1)
    assert test_data.url1 in driver.current_url
    logger.info("Test login successfully complete")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.critical
@pytest.mark.UI
def test_login_invalid_email(driver):
    """Test login with incorrect email"""
    lp = LoginPage(driver)
    lp.complete_login(test_data.invalid_eml, test_data.psw)
    assert lp.find_element_with_wait(error, 10)
    logger.info("Test login with incorrect email successfully complete")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.critical
@pytest.mark.UI
def test_login_invalid_password(driver):
    """Test login with incorrect password"""
    lp = LoginPage(driver)
    lp.complete_login(test_data.eml, test_data.invalid_psw)
    assert lp.find_element_with_wait(error, 10)
    logger.info("Test login with incorrect password"
                " successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_login_without_cred(driver):
    """Test login without entering credentials"""
    lp = LoginPage(driver)
    lp.click_login_button()
    assert lp.find_element_with_wait(error, 10)
    logger.info("Test login without entering credentials"
                " successfully complete")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_logout_success(driver, login_user):
    """Test logout successfully"""
    clp = ContactListPage(driver)
    clp.click_logout_button()
    lp = LoginPage(driver)
    assert lp.find_element_with_wait(email, 10)
    assert lp.find_element_with_wait(password, 10)
    logger.info("Test logout successfully complete")
