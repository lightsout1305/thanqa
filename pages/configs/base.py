"""
Модуль с базовым классом для конфигурации тест-кейса
"""
import typing
from abc import abstractmethod
from seleniumwire.webdriver import Chrome, Firefox, Edge


class BasePage:
    """
    Базовый класс для конфигурации тест-кейсов
    """
    # pylint: disable=too-few-public-methods

    def __init__(
            self, driver: typing.Union[Chrome, Firefox, Edge]) -> None:
        """
        Инициализация драйвера браузера
        :param driver: typing.Union[Chrome, Firefox, Edge]
        """
        self._validate_page(driver)
        self.driver: typing.Union[Chrome, Firefox, Edge] = driver

    @abstractmethod
    def _validate_page(
            self, driver: typing.Union[Chrome, Firefox, Edge]) -> None:
        """
        Метод валидации страницы
        :param driver: Chrome, Firefox, Edge
        :return: None
        """
        return


class InvalidPageException(Exception):
    """
    Класс-исключение невалидной страницы
    """
