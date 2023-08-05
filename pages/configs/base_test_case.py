"""
Общий для всех тестов модуль, содержащий класс BaseTestCase с общими для всех тестов настройками
"""
import typing
import unittest
import environ
from seleniumwire import webdriver
from seleniumwire.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions
from seleniumwire.webdriver import Chrome, Firefox, Edge, Remote
from selenium.webdriver.chrome.service import Service
from webdriver_manager.opera import OperaDriverManager


class BaseTestCase(unittest.TestCase):
    """
    Тест-кейс, который содержит общие для всех тест-кейсов конфигурации
    """
    BROWSER: str = 'chrome'
    PLATFORM: str = 'WINDOWS'
    driver: typing.Union[Chrome, Firefox, Edge, Remote]
    options: typing.Union[ChromeOptions, FirefoxOptions, EdgeOptions]

    env: environ.Env = environ.Env()
    env.read_env()

    def setUp(self) -> None:
        """
        Метод конфигурации тест-кейсов
        :return: None
        """
        url: typing.Optional[str] = self.env.str("DEV_URL")
        desired_caps: dict = \
            {"platformName": self.PLATFORM, "browserName": self.BROWSER}
        if desired_caps["browserName"] == "chrome":
            self.options: ChromeOptions = webdriver.ChromeOptions()
            self.options.add_argument("--ignore-ssl-errors=yes")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_experimental_option(
                "excludeSwitches", ["enable-logging"])
            self.driver: Chrome = webdriver.Chrome(
                options=self.options)
            self.driver.implicitly_wait(5)
            self.driver.maximize_window()
            self.driver.get(url)
        elif desired_caps["browserName"] == "firefox":
            self.options: FirefoxOptions = webdriver.FirefoxOptions()
            self.options.accept_insecure_certs = True
            self.driver: Firefox = webdriver.Firefox(options=self.options)
            self.driver.implicitly_wait(5)
            self.driver.maximize_window()
            self.driver.get(url)
        elif desired_caps["browserName"] == "MicrosoftEdge":
            self.options: EdgeOptions = webdriver.EdgeOptions()
            self.options.add_argument("--ignore-ssl-errors=yes")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_experimental_option(
                "excludeSwitches", ["enable-logging"])
            self.driver: Edge = webdriver.Edge(options=self.options)
            self.driver.implicitly_wait(5)
            self.driver.maximize_window()
            self.driver.get(url)
        else:
            self.options: ChromeOptions = webdriver.ChromeOptions()
            self.options.add_argument("--ignore-ssl-errors=yes")
            self.options.add_argument("--ignore-certificate-errors")
            self.options.add_argument("allow-elevated-browser")
            self.options.add_experimental_option("w3c", True)
            self.options.add_experimental_option(
                "excludeSwitches", ["enable-logging"])
            service: Service = Service(executable_path=OperaDriverManager().install())
            self.driver: Chrome = webdriver.Chrome(service=service, options=self.options)
            self.driver.implicitly_wait(5)
            self.driver.maximize_window()
            self.driver.get(url)

    def tearDown(self) -> None:
        """
        Выход из сессии браузера
        :return: None
        """
        self.driver.quit()
