from selenium.webdriver.common.by import By

from opencart.page_objects.base_page import BasePage
import allure

class CheckoutPage(BasePage):
    CHECKOUT_FORM = By.CSS_SELECTOR, "#checkout-checkout"
    CHECKOUT_PAYMENT_FORM = By.CSS_SELECTOR, "#checkout-payment-method"
    LOGIN_PAGE_LINK = By.XPATH, "//strong[text()='login page']"

    @allure.step("Выполняю проверку логин")
    def click_login_page_link(self):
        self.click(self.LOGIN_PAGE_LINK)

    @allure.step("Выполняю проверку загрузки страницы проверки данных")
    def wait_page_load(self):
        self.get_element(self.CHECKOUT_FORM)

    @allure.step("Выполняю проверку открытия страницы оплаты")
    def wait_payment_form(self):
        self.get_element(self.CHECKOUT_PAYMENT_FORM)
