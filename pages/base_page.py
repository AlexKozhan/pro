import allure
from playwright.sync_api import expect
from playwright.sync_api import Page  # Используем синхронный Page

from config import MAIN_PAGE_URL


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Opening url")
    def load(self):
        # Синхронный вызов для загрузки страницы
        self.page.goto(MAIN_PAGE_URL)

    def wait_url_contains(self, partial_url: str, timeout: int = 30000):
        """Ждет, пока URL будет содержать указанную подстроку."""
        # Синхронный вызов для ожидания URL
        self.page.wait_for_url(f"**{partial_url}**", timeout=timeout)

    def wait_for_value_in_element(self, selector: str, expected_value: str, timeout: int = 5000):
        """Ждет, пока значение элемента станет равным ожидаемому."""
        element = self.page.locator(selector)
        # Синхронный вызов для ожидания значения в элементе
        expect(element).to_have_value(expected_value, timeout=timeout)
