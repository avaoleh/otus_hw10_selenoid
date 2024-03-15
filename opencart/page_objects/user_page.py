import time
from selenium.webdriver.common.by import By

from opencart.page_objects.base_page import BasePage
from opencart.utils import helpers
import allure

cash_enum = ["€", "£", "$"]
cash_locators = [
    "(//ul[@class ='dropdown-menu show']/li)[1]",
    "(//ul[@class ='dropdown-menu show']/li)[2]",
    "(//ul[@class ='dropdown-menu show']/li)[3]",
]


class UserPage(BasePage):
    LOGIN_FORM = By.XPATH, "//*[@id='top']/div/div[2]/ul/li[2]/div/ul/li[2]/a"
    LOGIN_INPUT = By.CSS_SELECTOR, "#input-email"
    PASSWORD_INPUT = By.CSS_SELECTOR, "#input-password"
    SUBMIT_LOGIN_BUTTON = By.CSS_SELECTOR, "#form-login button"
    LOGOUT_LINK = By.LINK_TEXT, "Logout"
    USER_MENU = By.XPATH, "//*[@id='column-right']"
    WISH_LIST_LINK = By.XPATH, USER_MENU[1] + "//*[text()='Wish List']"

    AUTH_FORM = By.XPATH, "//*[@id='top']/div/div[2]/ul/li[2]/div/a"
    REG_BUTTON = By.XPATH, "//*[@id='top']/div/div[2]/ul/li[2]/div/ul/li[1]/a"
    FIRST_NAME = By.ID, "input-firstname"
    LAST_NAME = By.ID, "input-lastname"
    PASSWORD = By.ID, "input-password"
    EMAIL = By.ID, "input-email"
    POLICY = By.XPATH, '//*[@id="form-register"]/div/div/input'
    SUBMIT_AUTH_BUTTON = By.XPATH, '//*[@id="form-register"]/div/button'

    TITLE_TEXT = "Your Account Has Been Created!"

    CASH_SELECT = By.CSS_SELECTOR, ".dropdown"
    PRODUCT = By.CSS_SELECTOR, ".price-new"

    @allure.step("Выполняю проверку авторизации")
    def authorized(self, firstname, lastname, email, password):

        self.click(self.AUTH_FORM)
        self.click(self.REG_BUTTON)

        self.input_value(self.FIRST_NAME, firstname)
        self.input_value(self.LAST_NAME, lastname)
        self.input_value(self.EMAIL, email)
        self.input_value(self.PASSWORD, password)

        self.click(self.POLICY)
        self.click(self.SUBMIT_AUTH_BUTTON)

        self.wait_title_text(self.TITLE_TEXT)

        # helpers.clear_dir()
        # self.take_screenshot(helpers.path_src)

    @allure.step("Выполняю проверку логина")
    def login(self, username, password):
        self.click(self.AUTH_FORM)
        self.click(self.LOGIN_FORM)

        self.input_value(self.LOGIN_INPUT, username)
        self.input_value(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_LOGIN_BUTTON)

    @allure.step("Выполняю проверку логина")
    def login_by_proccesing(self, username, password):
        self.input_value(self.LOGIN_INPUT, username)
        self.input_value(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_LOGIN_BUTTON)
        return self

    def wait_logged_in(self):
        self.get_element(self.LOGOUT_LINK)
        return self

    @allure.step("Выполняю добавление в лист желаний")
    def click_wish_list(self):
        self.click(self.WISH_LIST_LINK)

    @allure.step("Выполняю проверку смены курса валют")
    def check_cash(self):
        for i in range(2):
            cash_select = self.browser.find_element(By.CSS_SELECTOR, ".dropdown")
            cash_select.click()

            cash_select_item = self.browser.find_element(By.XPATH, cash_locators[i])
            cash_select_item.click()
            product = self.browser.find_element(By.CSS_SELECTOR, ".price-new")

            if i == 0:
                assert product.text[-1] == cash_enum[i], f"Cash is {product.text[-1]}"
            else:
                assert product.text[0] == cash_enum[i], f"Cash is {product.text[0]}"
