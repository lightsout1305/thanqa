"""
Модуль с UI-тестами страницы авторизации
"""
import typing
import unittest
import environ
from seleniumwire import webdriver
from django.test import TestCase
from django.conf import settings
from seleniumwire.webdriver import Chrome, Firefox, Edge


class AuthPageTestCase(TestCase):
    """
    Тестирование страницы авторизации
    """
    env = environ.Env()
    env.read_env(settings.BASE_DIR, '.env')

    def setUp(self) -> None:
        """
        Создание тестовых данных для тестирования страницы авторизации
        :return: None
        """
        self.login: str = self.env.str("MAIL")
        self.password: str = self.env.str("PASSWORD")
        self.chrome_driver: typing.Type[Chrome] = webdriver.Chrome
        self.firefox_driver: typing.Type[Firefox] = webdriver.Firefox
        self.edge_driver: typing.Type[Edge] = webdriver.Edge
