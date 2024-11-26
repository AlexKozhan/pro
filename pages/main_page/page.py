import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.main_page.locators import MainPageLocators


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.PRODUCT_TITLE = page.locator(MainPageLocators.PRODUCT_TITLE)

    @allure.step("Checking whether product title is visible")
    def is_product_title_visible(self):
        return self.PRODUCT_TITLE.is_visible()
