





"""Base page"""
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import logger


class BasePage:
    """Class Base Page"""

    def __init__(self, driver):
        """Initializes an instance of the example Class"""
        self.driver = driver

    def open(self, url):
        """Get driver url method"""
        self.driver.get(url)

    def find_element(self, selector):
        """Find element method"""
        return self.driver.find_element(*selector)

    def find_element_with_wait(self, selector, timeout=3):
        """Find element with wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(selector)
            )
            return element
        except TimeoutException:
            logger.error(f"The element: {selector} wasn't found "
                         f"in {timeout} seconds.")
            return None

    def wait_value_in_element_appears(self, selector, text, timeout=3):
        """Wait until value in element appears"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(selector, text)
            )
            return True
        except TimeoutException:
            logger.info(f"The text: {text} wasn't"
                        f" appeared in: {selector}.")
            return False

    def wait_url(self, driver, data):
        """Wait until the URL contains the specified fragment"""
        try:
            WebDriverWait(driver, 10).until(EC.url_contains(data))
            return True
        except TimeoutException:
            logger.error(f"Operation timed out while waiting"
                         f" for the URL to contain {data}")
            return False
