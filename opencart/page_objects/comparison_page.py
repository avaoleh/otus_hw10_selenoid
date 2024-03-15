from selenium.webdriver.common.by import By

from opencart.page_objects.base_page import BasePage
import allure

class ComparisonPage(BasePage):
    CONFIRM_BUTTON = By.CSS_SELECTOR, "#button-confirm"

    def _product_name(self, product_name):
        return (By.XPATH, f"//*[@id='product-compare']//*[text()='{product_name}']")

    @allure.step("Выполняю проверку пападания продукта в список сравнения")
    def wait_for_product_in_comparison(self, product_name):
        self.get_element(self._product_name(product_name))
        return self

    @allure.step("Выполняю проверку нажатия на кнопку сравнения")
    def click_confirm(self):
        self.click(self.CONFIRM_BUTTON)
