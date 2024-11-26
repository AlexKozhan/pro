import allure
from playwright.sync_api import Page

from config import MAIN_PAGE_URL


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Opening url")
    def load(self):
        self.page.goto(MAIN_PAGE_URL)
