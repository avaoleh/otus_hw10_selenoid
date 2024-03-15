from selenium.webdriver.common.by import By

from opencart.page_objects.base_page import BasePage
import allure

class MainPage(BasePage):
    FEATURED_PRODUCT_NAME = By.CSS_SELECTOR, "#content > div.row .product-thumb h4 a"

    @allure.step("Выполняю поиск по элементу {selector}")
    def get_featured_product_name(self, index=0):
        return self.get_elements(self.FEATURED_PRODUCT_NAME)[index].text

    @allure.step("Выполняю клик по элементу {selector}")
    def click_featured_product(self, index=0):
        if index == 0:
            self.click(self.FEATURED_PRODUCT_NAME)
        else:
            self.get_elements(self.FEATURED_PRODUCT_NAME)[index].click()
