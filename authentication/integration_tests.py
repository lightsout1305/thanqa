"""
Модуль с интеграционными тестами страницы авторизации
"""
import json
import typing
import environ
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.request import Request
from pages.auth_page import AuthorizationPage
from pages.configs.base_test_case import BaseTestCase


class AuthPageTestCase(BaseTestCase):
    """
    Класс-дженерик тестирования авторизации
    """
    env = environ.Env()
    env.read_env()
    login: str = env.str("MAIL")
    password: str = env.str("PASSWORD")
    username: str = env.str("NICKNAME")

    def successful_authorization(self) -> None:
        """
        Тест-кейс-дженерик успешной авторизации
        :return: None
        """
        # Инициализация драйвера страницы авторизации
        auth_page: AuthorizationPage = AuthorizationPage(self.driver)
        auth_page.login(self.login)  # Ввести логин
        auth_page.password(self.password)  # Ввести пароль
        auth_page.enter()  # Нажать на кнопку Enter

        # Проверка метода Login после успешной авторизации
        # Ожидание вызова API login
        login_api: Request = auth_page.driver.wait_for_request(
            "http://127.0.0.1:8000/api/users/login/"
        )

        # Проверка, что метод login возвращает 200
        self.assertEqual(login_api.response.status_code, 200)

        # Тело запроса API login
        login_api_request_body: dict = json.loads(login_api.body.decode("utf-8"))

        # Тело ответа API login
        login_api_response_body: dict = json.loads(login_api.response.body.decode("utf-8"))

        # Проверка тела запроса API login
        # Проверка, что введенный E-mail передался в запрос
        self.assertEqual(login_api_request_body["user"]["email"], self.login)
        self.assertIsInstance(login_api_request_body["user"]["email"], str)

        # Проверка, что введенный пароль передался в запрос
        self.assertEqual(login_api_request_body["user"]["password"], self.password)
        self.assertIsInstance(login_api_request_body["user"]["password"], str)

        # Проверка тела ответа API login
        # Проверка, что сервер вернул E-mail пользователя
        self.assertEqual(login_api_response_body["user"]["email"], self.login)
        self.assertIsInstance(login_api_response_body["user"]["email"], str)

        # Проверка, что сервер вернул username пользователя
        self.assertEqual(login_api_response_body["user"]["username"], self.username)
        self.assertIsInstance(login_api_response_body["user"]["username"], str)

        # Проверка, что сервер вернул JWT-токен пользователя
        self.assertTrue(login_api_response_body["user"]["token"])
        self.assertIsInstance(login_api_response_body["user"]["token"], str)

        # Текст, который показывается на главной странице
        thanqa_title: typing.Any = self.driver.find_element(
            By.CLASS_NAME, 'thanqa-text'
        )

        # Проверка, что текст отображается, а значит пользователь авторизован
        self.assertEqual(thanqa_title.text, "Test Runs")

    def invalid_login_or_password(self) -> None:
        """
        Тест-кейс, что пользователь ввел неверный логин и/или пароль
        и не смог авторизоваться
        :return: None
        """
        # Инициализация драйвера страницы авторизации
        auth_page: AuthorizationPage = AuthorizationPage(self.driver)
        auth_page.login(self.login)  # Ввести правильный логин
        auth_page.password("sasasddfa")  # Ввести неправильный пароль
        auth_page.enter()  # Нажать на кнопку Enter

        # Ждем алерта с ошибкой
        WebDriverWait(auth_page.driver, 5).until(expected_conditions.visibility_of_element_located((
            By.ID, "errorNotification"
        )))

        # Инициализация алерта с ошибкой
        notification: typing.Any = auth_page.driver.find_element(
            By.ID, "errorNotification"
        )

        # Проверка, что алерт показывает ошибку неверного логина и/или пароля
        self.assertEqual(notification.text, "Invalid login or password")

        # Проверка метода login после неуспешной авторизации
        # Ожидание метода login
        login_api: Request = auth_page.driver.wait_for_request(
            "http://127.0.0.1:8000/api/users/login/"
        )

        # Проверка, что метод login возвращает 400
        self.assertEqual(login_api.response.status_code, 400)

        # Тело запроса API login
        login_api_request_body: dict = json.loads(login_api.body.decode("utf-8"))

        # Тело ответа API login
        login_api_response_body: dict = json.loads(login_api.response.body.decode("utf-8"))

        # Проверка тела запроса API login
        # Проверка, что введенный E-mail передался в запрос
        self.assertEqual(login_api_request_body["user"]["email"], self.login)
        self.assertIsInstance(login_api_request_body["user"]["email"], str)

        # Проверка, что введенный пароль передался в запрос
        self.assertEqual(login_api_request_body["user"]["password"], "sasasddfa")
        self.assertIsInstance(login_api_request_body["user"]["password"], str)

        # Проверка тела ответа API login
        # Проверка, что сервер ошибку неверного логина и/или пароля
        self.assertEqual(
            login_api_response_body["user"]["errors"]["error"][0], "Invalid login or password")

    def user_has_not_entered_login(self) -> None:
        """
        Тест-кейс, что пользователь не ввел логин
        и не смог авторизоваться
        :return: None
        """
        # Инициализация драйвера страницы авторизации
        auth_page: AuthorizationPage = AuthorizationPage(self.driver)
        auth_page.login(" ")  # Ввести пустой логин
        auth_page.password(self.password)  # Ввести неправильный пароль
        auth_page.enter()  # Нажать на кнопку Enter

        # Ждем алерта с ошибкой
        WebDriverWait(auth_page.driver, 5).until(expected_conditions.visibility_of_element_located((
            By.ID, "errorNotification"
        )))

        # Инициализация алерта с ошибкой
        notification: typing.Any = auth_page.driver.find_element(
            By.ID, "errorNotification"
        )

        # Проверка, что алерт показывает ошибку пустого логина
        self.assertEqual(notification.text, "Enter your E-mail")

        # Проверка метода login после неуспешной авторизации
        # Ожидание метода login
        login_api: Request = auth_page.driver.wait_for_request(
            "http://127.0.0.1:8000/api/users/login/"
        )

        # Проверка, что метод login возвращает 400
        self.assertEqual(login_api.response.status_code, 400)

        # Тело запроса API login
        login_api_request_body: dict = json.loads(login_api.body.decode("utf-8"))

        # Тело ответа API login
        login_api_response_body: dict = json.loads(login_api.response.body.decode("utf-8"))

        # Проверка тела запроса API login
        # Проверка, что введенный E-mail передался в запрос
        self.assertEqual(login_api_request_body["user"]["email"], " ")
        self.assertIsInstance(login_api_request_body["user"]["email"], str)

        # Проверка, что введенный пароль передался в запрос
        self.assertEqual(login_api_request_body["user"]["password"], self.password)
        self.assertIsInstance(login_api_request_body["user"]["password"], str)

        # Проверка тела ответа API login
        # Проверка, что сервер ошибку пустого логина
        self.assertEqual(
            login_api_response_body["user"]["errors"]["email"][0], "Enter your E-mail")

    def user_has_not_entered_password(self) -> None:
        """
        Тест-кейс, что пользователь не ввел пароль
        и не смог авторизоваться
        :return: None
        """
        # Инициализация драйвера страницы авторизации
        auth_page: AuthorizationPage = AuthorizationPage(self.driver)
        auth_page.login(self.login)  # Ввести логин
        auth_page.password(" ")  # Ввести пустой пароль
        auth_page.enter()  # Нажать на кнопку Enter

        # Ждем алерта с ошибкой
        WebDriverWait(auth_page.driver, 5).until(expected_conditions.visibility_of_element_located((
            By.ID, "errorNotification"
        )))

        # Инициализация алерта с ошибкой
        notification: typing.Any = auth_page.driver.find_element(
            By.ID, "errorNotification"
        )

        # Проверка, что алерт показывает ошибку пустого логина
        self.assertEqual(notification.text, "Enter your password")

        # Проверка метода login после неуспешной авторизации
        # Ожидание метода login
        login_api: Request = auth_page.driver.wait_for_request(
            "http://127.0.0.1:8000/api/users/login/"
        )

        # Проверка, что метод login возвращает 400
        self.assertEqual(login_api.response.status_code, 400)

        # Тело запроса API login
        login_api_request_body: dict = json.loads(login_api.body.decode("utf-8"))

        # Тело ответа API login
        login_api_response_body: dict = json.loads(login_api.response.body.decode("utf-8"))

        # Проверка тела запроса API login
        # Проверка, что введенный E-mail передался в запрос
        self.assertEqual(login_api_request_body["user"]["email"], self.login)
        self.assertIsInstance(login_api_request_body["user"]["email"], str)

        # Проверка, что введенный пароль передался в запрос
        self.assertEqual(login_api_request_body["user"]["password"], " ")
        self.assertIsInstance(login_api_request_body["user"]["password"], str)

        # Проверка тела ответа API login
        # Проверка, что сервер ошибку пустого пароля
        self.assertEqual(
            login_api_response_body["user"]["errors"]["password"][0], "Enter your password")


class TestAuthPageInChrome(AuthPageTestCase):
    """
    Тестирование страницы авторизации в Chrome
    """
    def test_successful_authorization_in_chrome(self) -> None:
        """
        Тест-кейс, что пользователь успешно авторизовался в Chrome
        :return: None
        """
        self.successful_authorization()

    def test_invalid_login_or_password_in_chrome(self) -> None:
        """
        Тест-кейс, что пользователь ввел неправильный логин и/или пароль
        в Chrome и не смог авторизоваться
        :return: None
        """
        self.invalid_login_or_password()

    def test_user_has_not_entered_login_in_chrome(self) -> None:
        """
        Тест-кейс, что пользователь не ввел логин в Chrome
        и не смог авторизоваться
        :return: None
        """
        self.user_has_not_entered_login()

    def test_user_has_not_entered_password_in_chrome(self) -> None:
        """
        Тест-кейс, что пользователь не ввел пароль в Chrome
        и не смог авторизоваться
        :return: None
        """
        self.user_has_not_entered_password()


class TestAuthPageInFirefox(AuthPageTestCase):
    """
    Тестирование страницы авторизации в Firefox
    """
    BROWSER = 'firefox'

    def test_successful_authorization_in_firefox(self) -> None:
        """
        Тест-кейс, что пользователь успешно авторизовался в Firefox
        :return:
        """
        self.successful_authorization()

    def test_invalid_login_or_password_in_firefox(self) -> None:
        """
        Тест-кейс, что пользователь ввел неправильный логин и/или пароль
        в Firefox и не смог авторизоваться
        :return: None
        """
        self.invalid_login_or_password()

    def test_user_has_not_entered_login_in_firefox(self) -> None:
        """
        Тест-кейс, что пользователь не ввел логин в Firefox
        и не смог авторизоваться
        :return: None
        """
        self.user_has_not_entered_login()

    def test_user_has_not_entered_password_in_firefox(self) -> None:
        """
        Тест-кейс, что пользователь не ввел пароль в Firefox
        :return: None
        """
        self.user_has_not_entered_password()


class TestAuthPageInEdge(AuthPageTestCase):
    """
    Тестирование страницы авторизации в Edge
    """
    BROWSER = 'MicrosoftEdge'

    def test_successful_authorization_in_edge(self) -> None:
        """
        Тест-кейс, что пользователь успешно авторизовался в Edge
        :return:
        """
        self.successful_authorization()

    def test_invalid_login_or_password_in_edge(self) -> None:
        """
        Тест-кейс, что пользователь ввел неправильный логин и/или пароль
        в Edge и не смог авторизоваться
        :return: None
        """
        self.invalid_login_or_password()

    def test_user_has_not_entered_login_in_edge(self) -> None:
        """
        Тест-кейс, что пользователь не ввел логин в Edge
        и не смог авторизоваться
        :return: None
        """
        self.user_has_not_entered_login()

    def test_user_has_not_entered_password_in_edge(self) -> None:
        """
        Тест-кейс, что пользователь не ввел пароль в Edge
        :return: None
        """
        self.user_has_not_entered_password()


class TestAuthPageInOpera(AuthPageTestCase):
    """
    Тестирование страницы авторизации в Opera
    """
    BROWSER = 'opera'

    def test_successful_authorization_in_opera(self) -> None:
        """
        Тест-кейс, что пользователь успешно авторизовался в Opera
        :return:
        """
        self.successful_authorization()

    def test_invalid_login_or_password_in_opera(self) -> None:
        """
        Тест-кейс, что пользователь ввел неправильный логин и/или пароль
        в Opera и не смог авторизоваться
        :return: None
        """
        self.invalid_login_or_password()

    def test_user_has_not_entered_login_in_opera(self) -> None:
        """
        Тест-кейс, что пользователь не ввел логин в Opera
        и не смог авторизоваться
        :return: None
        """
        self.user_has_not_entered_login()

    def test_user_has_not_entered_password_in_opera(self) -> None:
        """
        Тест-кейс, что пользователь не ввел пароль в Opera
        :return: None
        """
        self.user_has_not_entered_password()
