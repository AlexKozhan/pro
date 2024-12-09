"""Tests with Playwright"""
import pytest
import allure
from playwright.sync_api import expect
from pages.login_page.page import LoginPage
from pages.main_page.page import MainPage
from pages.contact_list_page.Contact_List_Page import ContactListPage
from config import USERNAME, PASSWORD
from pages.add_contact_page.add_contact_page import AddContactPage
from pages.contact_details_page.contact_details_page import ContactDetailsPage
from pages.edit_contact_page.edit_contact_page import EditContactPage
from Test_data import test_data
from logger import logger


import time

# Create a unique suffix using current timestamp or random number
unique_suffix = str(int(time.time()))  # Unique suffix to avoid conflict
test_data.fn = f"First_{unique_suffix}"
test_data.ln = f"Last_{unique_suffix}"


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.critical
@pytest.mark.UI
def test_add_contact(page):
    """Test add contact successfully"""
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)
    # Ждем окончания сетевой активности (если нужно)
    page.wait_for_load_state("networkidle", timeout=10000)
    # Последняя проверка на URL
    assert page.url == "https://thinking-tester-contact-list.herokuapp.com/contactList", \
        f"Expected URL: https://thinking-tester-contact-list.herokuapp.com/contactList, but got: {page.url}"

    # Клик по кнопке "Добавить контакт"
    page.wait_for_selector("text='Add a New Contact'", timeout=5000)
    page.click("text='Add a New Contact'")
    page.wait_for_url("**/addContact", timeout=5000)

    # Добавить контакт
    acp = AddContactPage(page)
    acp.add_contact(
        test_data.fn, test_data.ln, test_data.bd,
        test_data.eml1, test_data.pn, test_data.str1,
        test_data.str2, test_data.ct, test_data.stpr,
        test_data.pc, test_data.cntr
    )

    # Проверка на наличие ошибок JavaScript на странице после отправки формы
    page.on("console", lambda msg: logger.error(f"Console log: {msg.text}"))
    page.on("pageerror", lambda error: logger.error(f"Page error: {error}"))

    # Проверка ошибки 'undefined' на странице после отправки формы
    undefined_message = page.locator("text=undefined")
    if undefined_message.is_visible():
        logger.warning("'undefined' ошибка на странице после отправки формы, пропускаем выполнение.")
        page.screenshot(path="error_undefined_after_submit.png")
        page.wait_for_timeout(5000)  # Подождать немного, чтобы ошибка ушла, прежде чем продолжать

    # Увеличиваем время ожидания, чтобы данные успели сохраниться
    page.wait_for_timeout(10000)

    # Сделать снимок экрана для отладки
    page.screenshot(path="contact_list_page_before_check.png")

    # Перейти обратно на страницу списка контактов
    page.goto("https://thinking-tester-contact-list.herokuapp.com/contactList")
    page.wait_for_load_state("networkidle", timeout=30000)

    # Проверить наличие добавленного контакта
    contact_name = f"{test_data.fn} {test_data.ln}"
    row_locator = page.locator(f"tr.contactTableBodyRow:has-text('{contact_name}')")

    # Логирование количества строк
    all_rows = page.locator("tr.contactTableBodyRow")
    row_count = all_rows.count()
    logger.info(f"Всего строк найдено: {row_count}")

    # Убедиться, что нужная строка видима
    try:
        row_locator.wait_for(state="visible", timeout=30000)
        assert row_locator.is_visible(), f"Контакт {contact_name} не найден"
        logger.info(f"Контакт {contact_name} успешно добавлен.")
    except TimeoutError:
        logger.error(f"Контакт {contact_name} не найден на странице.")
        page.screenshot(path="contact_not_found_error.png")
        raise




@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_cancel_add_contact(page):
    """Test cancel add contact successfully"""
    clp = ContactListPage(page)
    clp.click_add_button()

    # Log current URL for debugging
    logger.info(f"Current URL after clicking add button: {page.url}")

    # Check if the URL contains the expected substring
    assert test_data.url_contain2 in page.url, f"Expected URL to contain {test_data.url_contain2}, but got {page.url}"

    acp = AddContactPage(page)
    acp.click_cancel_button()

    # Log current URL for debugging
    logger.info(f"Current URL after clicking cancel button: {page.url}")

    assert test_data.url1 in page.url, f"Expected URL to be {test_data.url1}, but got {page.url}"
    logger.info("Test cancel add contact successfully complete")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_edit_contact(page, created_contact):
    """Test editing a contact."""
    clp = ContactListPage(page)

    # Проверяем текущий URL перед редактированием контакта
    logger.info(f"Current URL before editing contact: {page.url}")
    if "addContact" in page.url:
        logger.info("Redirecting to the contact list page...")
        page.goto(test_data.url1)  # Явный переход на страницу списка контактов

    # Проверяем, что находимся на странице списка контактов
    page.wait_for_url(test_data.url1, timeout=10000)  # Ждём завершения перехода
    assert test_data.url1 in page.url, f"Expected URL to be {test_data.url1}, but got {page.url}"

    # Ищем добавленный контакт
    logger.info("Searching for the newly created contact...")
    contact_row = clp.find_contact_by_name("John", "Doe")
    assert contact_row is not None, "Contact not found!"

    # Начинаем редактирование контакта
    logger.info("Editing the contact...")
    contact_row.locator("button.editButton").click()
    acp = AddContactPage(page)
    acp.add_contact(
        fn="John",
        ln="Doe",
        bd="1990-01-01",
        eml1="john.doe@example.com",
        pn="123456789",
        str1="123 Main St",
        str2="Apt 4B",  # Указываем str2
        ct="New York",
        stpr="NY",
        pc="10001",
        cntr="USA"
    )

    # Проверяем, что контакт был успешно обновлён
    logger.info("Verifying the updated contact...")
    updated_contact = clp.find_contact_by_name("Jane", "Smith")
    assert updated_contact is not None, "Updated contact not found!"
    logger.info("Test edit contact successfully complete.")



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
