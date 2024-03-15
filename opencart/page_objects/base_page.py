from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging

class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.logger = browser.logger
        self.class_name = type(self).__name__

    def open(self, url):
        self.browser.get(url)

    def _text_xpath(self, text):
        return f"//*[text()='{text}']"

    def get_element(self, locator: tuple, timeout=3):
        self.logger.debug("%s: Getting element: %s" % (self.class_name, str(locator)))
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def get_elements(self, locator: tuple, timeout=3):
        self.logger.debug("%s: Getting elements: %s" % (self.class_name, str(locator)))
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def click_element_clickable(self, locator: tuple, timeout=3):
        self.logger.debug("%s: Clicking clickable element: %s" % (self.class_name, str(locator)))
        return WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_title_text(self, text, timeout=3):
        self.logger.debug("%s: Waiting element: %s" % (self.class_name, str(text)))
        return WebDriverWait(self.browser, timeout).until(EC.title_is(text))

    def take_screenshot(self, path):
        self.browser.save_screenshot(path)

    def click(self, locator: tuple):
        self.logger.debug("%s: Click element: %s" % (self.class_name, str(locator)))
        ActionChains(self.browser).move_to_element(self.get_element(locator)).pause(
            0.3
        ).click().perform()

    def input_value(self, locator: tuple, text: str):
        self.logger.debug("%s: Input value: %s" % (self.class_name, str(locator)))
        self.get_element(locator).click()
        self.get_element(locator).clear()
        for l in text:
            self.get_element(locator).send_keys(l)
