"""
Объект страницы авторизации
"""
import time
import typing
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pages.configs.base import InvalidPageException, BasePage


class AuthorizationPage(BasePage):
    """
    Страница авторизации
    """
    __auth_page_login_locator: typing.ClassVar[str] = "//input[@placeholder='Enter your E-mail']"
    __auth_page_password_locator: typing.ClassVar[str] = "//input[@type='password']"
    __auth_page_enter_button_locator: typing.ClassVar[str] = "enterButton"
    __auth_page_forgot_button: typing.ClassVar[str] = "forgot-password"

    def _validate_page(self, driver: typing.Any) -> None:
        """
        Проверка, что страница авторизации загружена
        :param driver: WebDriver()
        :return: None
        """
        try:
            driver.find_element(By.XPATH, self.__auth_page_login_locator)
            driver.find_element(By.XPATH, self.__auth_page_password_locator)
            driver.find_element(By.ID, self.__auth_page_enter_button_locator)
        except InvalidPageException:
            print('Страница авторизации не была загружена')

    def login(self, login: typing.Optional[str]) -> None:
        """
        Ввод в поле логина
        :param login: str
        :return: None
        """
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//input[@placeholder='Enter your E-mail']"
            )))
        __login_field: typing.Any = self.driver.find_element(
            By.XPATH, self.__auth_page_login_locator)
        __login_field.clear()
        time.sleep(1)
        __login_field.send_keys(login)

    def password(self, password: typing.Optional[str]) -> None:
        """
        Ввод в поле пароля
        :param password: str
        :return: None
        """
        __password_field: typing.Any = self.driver.find_element(
            By.XPATH, self.__auth_page_password_locator)
        __password_field.clear()
        time.sleep(1)
        __password_field.send_keys(password)

    def enter(self) -> None:
        """
        Нажатие на кнопку "Enter"
        :return: None
        """
        __enter_button: typing.Any = self.driver.find_element(
            By.ID, self.__auth_page_enter_button_locator)
        __enter_button.click()
        time.sleep(1)

    def forgot_password(self) -> None:
        """
        Нажатие на кнопку "Forgot your password?"
        :return: None
        """
        __forgot_password_button: typing.Any = self.driver.find_element(
            By.XPATH, self.__auth_page_forgot_button)
        __forgot_password_button.click()
