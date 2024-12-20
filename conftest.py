import uuid
import pytest
import allure
from playwright.sync_api import Browser, BrowserContext
from pages.login_page.page import LoginPage
from config import USERNAME, PASSWORD
from pages.add_contact_page.add_contact_page import AddContactPage
from pages.contact_list_page.Contact_List_Page import ContactListPage
from pages.contact_details_page.contact_details_page import ContactDetailsPage
from Test_data import test_data
from logger import logger
# from playwright.sync_api import sync_playwright


# Генерация уникального email
@pytest.fixture(scope="session")
def unique_email() -> str:
    """Fixture to generate a unique email"""
    return f"{uuid.uuid4()}@example.com"


# Настроим размеры экрана для браузера
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        'viewport': {
            'width': 800,
            'height': 600,
        },
    }


# Фикстура для контекста браузера с сохранением состояния
@pytest.fixture(scope="session")
def context(create_browser_context, browser: Browser,
            browser_context_args: dict) -> BrowserContext:
    context = browser.new_context(storage_state="./state.json",
                                  **browser_context_args)
    yield context
    context.close()


# Фикстура для страницы
# @pytest.fixture(scope="function")
# def page():
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         yield page
#         browser.close()


# Фикстура для создания контекста и авторизации
@allure.step("Create Session")
@pytest.fixture(scope='session')
def create_browser_context(browser) -> None:
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)

    yield context, page
    context.close()


# Фикстура для создания контакта
@pytest.fixture()
def created_contact(page):
    """Fixture to create a contact in the UI."""
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)

    # Ждем окончания сетевой активности
    page.wait_for_load_state("networkidle", timeout=10000)

    # Последняя проверка на URL
    assert page.url == ("https://thinking-tester-contact"
                        "-list.herokuapp.com/contactList"), \
        (f"Expected URL: https://thinking-tester-contact-list."
         f"herokuapp.com/contactList, but got: {page.url}")

    # Клик по кнопке "Добавить контакт"
    page.wait_for_selector("text='Add a New Contact'", timeout=5000)
    page.click("text='Add a New Contact'")
    page.wait_for_url("**/addContact", timeout=5000)

    # Создаём контакт
    add_contact_page = AddContactPage(page)
    add_contact_page.add_contact(
        fn="John", ln="Doe", bd="1990-01-01",
        eml1="john.doe@example.com", pn="123456789",
        str1="123 Main St", str2="123 Main St", ct="New York",
        stpr="NY",
        pc="10001", cntr="USA"
    )

    page.on("console", lambda msg: logger.error
    (f"Console log: {msg.text}"))
    page.on("pageerror", lambda error: logger.error
    (f"Page error: {error}"))

    undefined_message = page.locator("text=undefined")
    if undefined_message.is_visible():
        logger.warning("'undefined' ошибка на странице после "
                       "отправки формы, пропускаем выполнение.")
        page.wait_for_timeout(5000)

    page.wait_for_timeout(10000)

    page.goto("https://thinking-tester-contact-list.herokuapp.com"
              "/contactList")
    page.wait_for_load_state("networkidle", timeout=30000)

    # Логируем текущий URL после добавления контакта
    logger.info(f"Current URL after adding contact: {page.url}")

    page.wait_for_url(test_data.url1, timeout=30000)
    logger.info("Returned to the contact list page successfully.")

    # Формируем имя контакта для поиска
    contact_name = "John Doe"
    row_locator = page.locator(f"tr.contactTableBodyRow:has-text"
                               f"('{contact_name}')")

    # Логирование количества строк
    all_rows = page.locator("tr.contactTableBodyRow")
    row_count = all_rows.count()
    logger.info(f"Всего строк найдено: {row_count}")

    # Убедиться, что нужная строка видима
    try:
        row_locator.wait_for(state="visible", timeout=30000)
        assert row_locator.is_visible(), (f"Контакт "
                                          f"{contact_name} не найден")
        logger.info(f"Контакт {contact_name} успешно добавлен.")
    except TimeoutError:
        logger.error(f"Контакт {contact_name} не найден на странице.")
        raise

    return add_contact_page


@pytest.fixture(scope="session")
def existing_email():
    """Fixture to provide an existing email for testing"""
    return "john.doe112111@example.com"


@pytest.fixture(scope="function")
def delete_contact_after_test(page):
    """Фикстура для удаления контакта после теста"""

    def _delete_contact(contact_name):
        contact_list_page = ContactListPage(page)

        # Ищем строку с данным контактом на странице списка
        row_locator = page.locator(f"tr.contactTableBodyRow:"
                                   f"has-text('{contact_name}')")
        row_locator.wait_for(state="visible", timeout=5000)
        row_locator.click()

        # Создаем объект для страницы деталей контакта
        cdp = ContactDetailsPage(page)

        # Логируем начало процесса удаления
        logger.info(f"Deleting the contact: {contact_name}...")

        page.on('dialog', lambda dialog: dialog.accept())

        # Кликаем на кнопку "Delete Contact"
        cdp.click_delete_button()

        page.wait_for_timeout(5000)

        # Проверяем, что контакт исчез с текущей страницы
        row_locator = page.locator(f"tr.contactTableBodyRow:"
                                   f"has-text('{contact_name}')")
        try:
            # Проверяем, что контакт исчез с страницы
            row_locator.wait_for(state="detached", timeout=10000)
            logger.info(f"Контакт {contact_name} успешно удален.")
        except TimeoutError:
            logger.error(f"Контакт {contact_name} не был удален!")
            raise

        # Проверяем, что страница вернулась на список контактов
        assert page.url == ("https://thinking-tester-contact-list."
                            "herokuapp.com/contactList"), "Deletion failed!"

    yield _delete_contact
