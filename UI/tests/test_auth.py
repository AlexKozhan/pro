import allure
import pytest
from pages.login_page.page import LoginPage
from pages.contact_list_page.Contact_List_Page import ContactListPage
from config import USERNAME, PASSWORD
from pages.main_page.page import MainPage
from logger import logger
from playwright.sync_api import Page



@allure.title("Login test")
@allure.description("This test logs into the system and checks the opening of the main page")
def test_login(page):
    main_page = MainPage(page)
    main_page.load()
    assert main_page.is_product_title_visible(), "Product title is not visible"


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_login_success(page: Page):
    """Test login successfully based on URL change"""

    # Создаем объект страницы логина и выполняем вход
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)
    # Ждем окончания сетевой активности (если нужно)
    page.wait_for_load_state("networkidle", timeout=10000)
    # Последняя проверка на URL
    assert page.url == "https://thinking-tester-contact-list.herokuapp.com/contactList", \
        f"Expected URL: https://thinking-tester-contact-list.herokuapp.com/contactList, but got: {page.url}"


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.critical
@pytest.mark.UI
def test_login_invalid_email(page):
    """Test login with incorrect email"""
    login_page = LoginPage(page)
    login_page.login("invalid@example.com", PASSWORD)
    page.wait_for_load_state("domcontentloaded", timeout=10000)
    assert login_page.is_error_message_visible(), "Error message not visible"
    logger.info("Test login with incorrect email successfully complete")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.critical
@pytest.mark.UI
def test_login_invalid_password(page):
    """Test login with incorrect password"""
    login_page = LoginPage(page)
    login_page.login(USERNAME, "invalidpassword")

    assert login_page.is_error_message_visible(), "Error message not visible"
    logger.info("Test login with incorrect password successfully complete")


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_login_without_cred(page):
    """Test login without entering credentials"""
    login_page = LoginPage(page)

    # Нажимаем кнопку без ввода данных
    login_page.login(" ", " ")

    # Подождите немного, чтобы ошибка могла отобразиться
    page.wait_for_timeout(5000)  # Ожидаем 5 секунды

    # Выведем доступные элементы для отладки
    print("Page content after login attempt:", page.content())

    # Проверим, что ошибка отображается на странице логина
    assert login_page.is_error_message_visible(), "Error message not visible"

    # Проверим, что форма логина остается на месте и кнопка не исчезла
    assert login_page.is_login_button_visible(), "Login button not visible after attempting login without credentials"

    # Также можно проверить, что мы остались на странице логина, а не перенаправились на страницу контактов
    assert page.url == "https://thinking-tester-contact-list.herokuapp.com/", \
        f"Expected URL to be the login page, but got {page.url}"

    logger.info("Test login without entering credentials successfully completed")


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_logout_success(page):
    """Test logout successfully"""
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)
    page.wait_for_load_state("networkidle", timeout=10000)
    contact_list_page = ContactListPage(page)
    contact_list_page.click_logout_button()

    # Wait for the page to transition back to the login page
    page.wait_for_load_state("networkidle", timeout=10000)

    # Check the visibility of the login button
    assert login_page.is_login_button_visible(), "Logout button not visible after logout"


