"""Tests with Playwright"""
import pytest
import allure
from pages.login_page.page import LoginPage
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
def test_add_contact(page, delete_contact_after_test):
    """Test add contact successfully"""
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)
    # Ждем окончания сетевой активности (если нужно)
    page.wait_for_load_state("networkidle", timeout=10000)
    # Последняя проверка на URL
    assert page.url == ("https://thinking-tester-contact-list"
                        ".herokuapp.com/contactList"), \
        (f"Expected URL: https://thinking-tester-contact-list"
         f".herokuapp.com/contactList, but got: {page.url}")

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
        logger.warning("'undefined' ошибка на странице после "
                       "отправки формы, пропускаем выполнение.")
        page.wait_for_timeout(5000)

    # Увеличиваем время ожидания, чтобы данные успели сохраниться
    page.wait_for_timeout(10000)

    # Перейти обратно на страницу списка контактов
    page.goto("https://thinking-tester-contact-list"
              ".herokuapp.com/contactList")
    page.wait_for_load_state("networkidle", timeout=30000)

    # Проверить наличие добавленного контакта
    contact_name = f"{test_data.fn} {test_data.ln}"
    row_locator = page.locator(f"tr.contactTableBodyRow:"
                               f"has-text('{contact_name}')")

    # Логирование количества строк
    all_rows = page.locator("tr.contactTableBodyRow")
    row_count = all_rows.count()
    logger.info(f"Всего строк найдено: {row_count}")
    page.reload()

    # Убедиться, что нужная строка видима
    try:
        row_locator.wait_for(state="visible", timeout=40000)
        assert row_locator.is_visible(), f"Контакт {contact_name} не найден"
        logger.info(f"Контакт {contact_name} успешно добавлен.")
    except TimeoutError:
        logger.error(f"Контакт {contact_name} не найден на странице.")
        page.screenshot(path="contact_not_found_error.png")
        raise


    delete_contact_after_test(contact_name)
    logger.info("Contact successfully deleted.")



@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_cancel_add_contact(page):
    """Test cancel add contact successfully"""
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)
    # Ждем окончания сетевой активности (если нужно)
    page.wait_for_load_state("networkidle", timeout=10000)
    # Последняя проверка на URL
    assert page.url == ("https://thinking-tester-contact-list"
                        ".herokuapp.com/contactList"), \
        (f"Expected URL: https://thinking-tester-contact-list"
         f".herokuapp.com/contactList, but got: {page.url}")

    # Клик по кнопке "Добавить контакт"
    page.wait_for_selector("text='Add a New Contact'", timeout=5000)
    page.click("text='Add a New Contact'")
    page.wait_for_url("**/addContact", timeout=5000)


    logger.info(f"Current URL after clicking add button: {page.url}")

    # Check if the URL contains the expected substring
    assert test_data.url_contain2 in page.url, \
        (f"Expected URL to contain {test_data.url_contain2}, "
         f"but got {page.url}")

    acp = AddContactPage(page)
    acp.click_cancel_button()

    # Log current URL for debugging
    logger.info(f"Current URL after clicking cancel button: {page.url}")

    assert test_data.url1 in page.url, \
        f"Expected URL to be {test_data.url1}, but got {page.url}"
    logger.info("Test cancel add contact successfully complete")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_edit_contact(page, created_contact, delete_contact_after_test):
    """Test editing a contact."""
    ecp = EditContactPage(page)

    # Ищем добавленный контакт
    logger.info("Searching for the newly created contact...")
    contact_name1 = "John Doe"  # Контакт, который был создан
    row_locator1 = page.locator(f"tr.contactTableBodyRow:"
                                f"has-text('{contact_name1}')")

    # Проверяем, что контакт найден
    assert row_locator1 is not None, "Contact not found!"
    row_locator1.click()

    # Начинаем редактирование контакта
    logger.info("Editing the contact...")
    page.locator("xpath=//button[text()='Edit Contact']").click()

    # Редактируем контакт
    ecp.edit_contact(
        fn_1="Jane",
        ln_1="Smith",
        bd_1="1990-02-04",
        eml1_1="john.doe@example.com",
        pn_1="123456789",
        str1_1="123 Main St",
        str2_1="Apt 4B",  # Указываем str2
        ct_1="New York",
        stpr_1="NY",
        pc_1="10001",
        cntr_1="USA"
    )

    # Переходим обратно на страницу списка контактов
    page.goto("https://thinking-tester-contact-list"
              ".herokuapp.com/contactList")
    page.wait_for_load_state("networkidle", timeout=10000)

    # Проверяем, что контакт был успешно обновлён
    logger.info("Verifying the updated contact...")
    updated_contact_name = "Jane Smith"  # Новый контакт
    updated_row_locator = (
        page.locator(f"tr.contactTableBodyRow:has-text('{updated_contact_name}')"))

    # Убедиться, что обновлённый контакт видим
    try:
        updated_row_locator.wait_for(state="visible", timeout=30000)
        assert updated_row_locator.is_visible(), \
            f"Updated contact {updated_contact_name} not found!"
        logger.info(f"Contact {contact_name1} successfully updated.")
    except TimeoutError:
        logger.error(f"Updated contact {updated_contact_name} not found!")
        page.screenshot(path="updated_contact_not_found_error.png")
        raise

    logger.info("Test edit contact successfully complete.")
    delete_contact_after_test(updated_contact_name)
    if updated_row_locator.is_visible():
        delete_contact_after_test(updated_contact_name)
    logger.info("Contact successfully deleted.")



@allure.severity(allure.severity_level.MINOR)
@pytest.mark.extended
@pytest.mark.UI
def test_cancel_edit_contact(page, created_contact,
                             delete_contact_after_test):
    """Test cancel edit contact successfully"""
    ecp = EditContactPage(page)

    # Ищем добавленный контакт
    logger.info("Searching for the newly created contact...")
    contact_name1 = "John Doe"  # Контакт, который был создан
    row_locator1 = (page.locator
                    (f"tr.contactTableBodyRow:has-text('{contact_name1}')"))

    # Проверяем, что контакт найден
    assert row_locator1 is not None, "Contact not found!"
    row_locator1.click()

    # Начинаем редактирование контакта
    logger.info("Editing the contact...")
    page.locator("xpath=//button[text()='Edit Contact']").click()

    ecp.click_cancel_button()

    # Ожидаем появления элемента с id="firstName"
    ecp.page.locator("span#firstName").wait_for(timeout=5000)

    # Получаем текущее значение поля firstName и проверяем его
    current_value = ecp.page.locator("span#firstName").text_content()
    assert current_value == 'John', (f"Expected 'John', "
                                     f"but got {current_value}")

    expected_result = [
        "John", "Doe", "1990-01-01",
        "john.doe@example.com", "123456789",
        "123 Main St", "123 Main St", "New York", "NY",
        "10001", "USA"
    ]

    cdp = ContactDetailsPage(page)
    actual_result = cdp.get_all_contact_details_data()
    assert actual_result == expected_result

    cdp.click_return_button()
    logger.info("Test cancel edit contact successfully complete")
    delete_contact_after_test(contact_name1)
    logger.info("Contact successfully deleted.")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.UI
def test_delete_contact(page, created_contact):
    """Test delete contact successfully"""

    cdp = ContactDetailsPage(page)

    # Ищем добавленный контакт
    logger.info("Searching for the newly created contact...")
    contact_name1 = "John Doe"  # Контакт, который был создан
    row_locator1 = (
        page.locator(f"tr.contactTableBodyRow:has-text('{contact_name1}')"))

    # Проверяем, что контакт найден
    assert row_locator1 is not None, "Contact not found!"
    row_locator1.click()

    # Начинаем редактирование контакта
    logger.info("Deleting the contact...")

    # Слушаем событие диалога и автоматически подтверждаем его
    page.on('dialog', lambda dialog: dialog.accept())

    # Кликаем на кнопку "Delete Contact"
    cdp.click_delete_button()

    # Логируем, чтобы понять, что произошло
    logger.info("Delete button clicked. Waiting for response...")

    # Ожидаем, что контакт удалится
    page.wait_for_timeout(2000)

    # Проверяем, что контакт исчез с текущей страницы
    row_locator1 = page.locator(f"tr.contactTableBodyRow:has-text('{contact_name1}')")
    assert row_locator1.count() == 0, "Contact not deleted from the page!"

    # Проверяем, что страница вернулась на список контактов
    assert page.url == ("https://thinking-tester-contact-list"
                        ".herokuapp.com/contactList"), "Deletion failed!"
    logger.info("Contact is deleted successfully!")
