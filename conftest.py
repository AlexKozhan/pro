import uuid
import pytest
import allure
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Playwright, APIRequestContext, Page
from pages.login_page.page import LoginPage
from config import USERNAME, PASSWORD
from pages.contact_list_page.Contact_List_Page import ContactListPage
from pages.add_contact_page.add_contact_page import AddContactPage
from pages.contact_details_page.contact_details_page import ContactDetailsPage


# Генерация уникального email
@pytest.fixture(scope="session")
def unique_email() -> str:
    """Fixture to generate a unique email"""
    return f"{uuid.uuid4()}@example.com"


# Настроим размеры экрана для браузера
@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        'viewport': {
            'width': 800,
            'height': 600,
        },
    }


# Фикстура для контекста браузера с сохранением состояния
@pytest.fixture()
def context(create_browser_context, browser: Browser, browser_context_args: dict) -> BrowserContext:
    context = browser.new_context(storage_state="state.json", **browser_context_args)
    yield context
    context.close()


# Фикстура для страницы
@pytest.fixture(scope="function")
def page(create_browser_context) -> Page:
    context, page = create_browser_context  # Возвращаем пару (context, page)
    yield page
    page.close()


# Фикстура для создания контекста и авторизации
@allure.step("Create Session")
@pytest.fixture(scope='session')
def create_browser_context(browser) -> None:
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)
    context.storage_state(path="state.json")  # Сохраняем состояние
    yield context, page
    context.close()


# Фикстура для работы с API запросами
@pytest.fixture(scope="session")
def api_request_context(
        playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url="https://petstore.swagger.io/"
    )
    yield request_context
    request_context.dispose()


# Фикстура для создания контакта
@pytest.fixture()
def created_contact(page):
    """Fixture to create a contact in the UI."""
    login_page = LoginPage(page)
    login_page.login(USERNAME, PASSWORD)

    contact_list_page = ContactListPage(page)
    contact_list_page.click_add_button()

    # Создание контакта
    add_contact_page = AddContactPage(page)
    add_contact_page.add_contact(
        first_name="John",
        last_name="Doe",
        birthdate="01-01-1990",
        email="john.doe@example.com",
        phone="123456789",
        street="123 Main St",
        city="New York",
        state="NY",
        postal_code="10001",
        country="USA"
    )
    add_contact_page.wait_for_contact_to_appear()  # Подождем, пока контакт появится в списке

    yield add_contact_page  # Возвращаем объект страницы для теста

    # Удаляем контакт после теста
    contact_details_page = ContactDetailsPage(page)
    contact_details_page.click_delete_button()
    contact_list_page.wait_for_contact_to_disappear()  # Убедимся, что контакт удален


# Снимки экрана и HTML исходного кода при ошибках
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    test_result = outcome.get_result()
    test_result.extra = []

    # Если фикстура page не найдена в тесте
    if "page" not in item.funcargs:
        return

    page = item.funcargs["page"]

    if test_result.when in ["setup", "call"]:
        xfail = hasattr(test_result, 'wasxfail')



@pytest.fixture(scope="session")
def existing_email():
    """Fixture to provide an existing email for testing"""
    return "john.doe112111@example.com"
