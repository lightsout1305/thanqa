"""
Модуль с тестами приложения api
"""
import requests
import environ
from django.test import TestCase
from requests import Response
from requests.auth import AuthBase
from thanqa_tms.settings import BASE_DIR


class BearerAuth(AuthBase):
    """
    Авторизация с помощью токена
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["authorization"] = "Bearer " + self.token
        return request


class TestLogin(TestCase):
    """
    Тестирование метода Login
    """
    env: environ.Env = environ.Env()
    env.read_env(BASE_DIR, ".env")

    def setUp(self) -> None:
        """
        Создание тестовых данных для тестирования Login
        :return: None
        """
        self.correct_email: str = self.env.str("MAIL")
        self.correct_password: str = self.env.str("PASSWORD")
        self.username: str = self.env.str("NICKNAME")
        self.incorrect_email: str = "test@example.com"
        self.incorrect_password: str = "test123"

    def test_login_returns_200_and_has_necessary_fields(self) -> None:
        """
        Тест-кейс успешной авторизации.
        1. Статус-код 200
        2. У метода необходимые поля
        3. У метода необходимые типы данных
        :return: None
        """
        login_api: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": self.correct_email,
                    "password": self.correct_password
                }
            }, timeout=10)
        self.assertEqual(login_api.status_code, 200)
        self.assertEqual(login_api.json()["user"]["email"], self.correct_email)
        self.assertEqual(login_api.json()["user"]["username"], self.username)
        self.assertTrue(login_api.json()["user"]["token"])
        self.assertIsInstance(login_api.json()["user"]["email"], str)
        self.assertIsInstance(login_api.json()["user"]["username"], str)
        self.assertIsInstance(login_api.json()["user"]["token"], str)

    def test_login_returns_400_if_incorrect_login_or_password(self) -> None:
        """
        Тест-кейс неуспешной авторизации, если логин и/или пароль неверны.
        1. Статус-код 400
        2. Сервер возвращает информацию об ошибке
        :return: None
        """
        login_api_with_incorrect_email: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": self.incorrect_email,
                    "password": self.correct_password
                }
            }, timeout=10)
        self.assertEqual(login_api_with_incorrect_email.status_code, 400)
        self.assertEqual(login_api_with_incorrect_email.json()["user"]["errors"]["error"][0],
                         "Invalid login or password")

        login_api_with_incorrect_password: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": self.correct_email,
                    "password": self.incorrect_password
                }
            }, timeout=10)
        self.assertEqual(login_api_with_incorrect_password.status_code, 400)
        self.assertEqual(login_api_with_incorrect_password.json()["user"]["errors"]["error"][0],
                         "Invalid login or password")

        login_api_with_both_incorrect_email_and_password: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": self.incorrect_email,
                    "password": self.incorrect_password
                }
            }, timeout=10)
        self.assertEqual(login_api_with_both_incorrect_email_and_password.status_code, 400)
        self.assertEqual(login_api_with_both_incorrect_email_and_password.json()
                         ["user"]["errors"]["error"][0],
                         "Invalid login or password")

    def test_login_api_returns_400_if_login_or_password_is_null(self) -> None:
        """
        Тест-кейс неуспешной авторизации, если логин и/или пароль не указаны.
        1. Статус-код 400
        2. Сервер возвращает информацию об ошибке
        :return: None
        """
        login_api_with_no_email: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": None,
                    "password": self.correct_password
                }
            }, timeout=10)
        self.assertEqual(login_api_with_no_email.status_code, 400)
        self.assertEqual(login_api_with_no_email.json()["user"]["errors"]["email"][0],
                         "Enter your E-mail")

        login_api_with_no_password: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": self.correct_email,
                    "password": None
                }
            }, timeout=10)
        self.assertEqual(login_api_with_no_password.status_code, 400)
        self.assertEqual(login_api_with_no_password.json()["user"]["errors"]["password"][0],
                         "Enter your password")

        login_api_with_no_email_and_password: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": None,
                    "password": None
                }
            }, timeout=10)
        self.assertEqual(login_api_with_no_email_and_password.status_code, 400)
        self.assertEqual(login_api_with_no_email_and_password.json()["user"]["errors"]["email"][0],
                         "Enter your E-mail")
        self.assertEqual(login_api_with_no_email_and_password.json()
                         ["user"]["errors"]["password"][0],
                         "Enter your password")

        login_api_with_blank_email: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": "",
                    "password": self.correct_password
                }
            }, timeout=10)
        self.assertEqual(login_api_with_blank_email.status_code, 400)
        self.assertEqual(login_api_with_blank_email.json()["user"]["errors"]["email"][0],
                         "Enter your E-mail")

        login_api_with_blank_password: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": self.correct_email,
                    "password": ""
                }
            }, timeout=10)
        self.assertEqual(login_api_with_blank_password.status_code, 400)
        self.assertEqual(login_api_with_blank_password.json()["user"]["errors"]["password"][0],
                         "Enter your password")

        login_api_with_both_blank_email_and_password: Response = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": "",
                    "password": ""
                }
            }, timeout=10)
        self.assertEqual(login_api_with_both_blank_email_and_password.status_code, 400)
        self.assertEqual(login_api_with_both_blank_email_and_password.json()
                         ["user"]["errors"]["email"][0],
                         "Enter your E-mail")
        self.assertEqual(login_api_with_both_blank_email_and_password.json()
                         ["user"]["errors"]["password"][0],
                         "Enter your password")


class TestCreateTestPlan(TestCase):
    """
    Тестирование метода CreateTestPlan
    """
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=too-many-instance-attributes

    env: environ.Env = environ.Env()
    env.read_env(BASE_DIR, ".env")

    def setUp(self) -> None:
        """
        Инициализация тестовых данных
        :return: None
        """
        self.title: str = "Релиз-план 2023.16 по функционалу добавления/редактирования" \
                          "/прочтения/удаления тест-плана"
        with open('./description_for_test_plan.txt', encoding='utf-8') as file:
            self.description = file.read()
        self.author: int = 1
        self.is_current: bool = True
        self.testing_start_date: str = "2023-08-23T20:38:43.469088Z"
        self.testing_end_date: str = "2023-08-30T20:38:43.469088Z"
        self.wrong_testing_end_date: str = "2023-07-30T20:38:43.469088Z"
        self.correct_email: str = self.env.str("MAIL")
        self.correct_password: str = self.env.str("PASSWORD")
        self.headers_auth = {"Authorization": "Bearer " + ""}
        self.token: str = \
            requests.post("http://127.0.0.1:8000/api/users/login/", json={
                "user": {
                    "email": self.correct_email,
                    "password": self.correct_password
                }
            }, timeout=10).json()["user"]["token"]
        self.successful_data: dict
        self.successful_create_test_plan: Response
        self.successful_data_with_only_title: dict
        self.unsuccessful_create_test_plan: Response

    def test_create_test_plan_returns_200(self) -> None:
        """
        Тест-кейс, что метод добавления тест-плана возвращает 200
        и создает тест-план, если все поля введены.
        :return: None
        """
        self.successful_data = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.successful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.successful_data,
            timeout=10
        )
        self.assertEqual(self.successful_create_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["title"], self.title)
        self.assertIsInstance(
            self.successful_create_test_plan.json()["test_plan"]["title"], str)
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["is_current"], self.is_current
        )
        self.assertIsInstance(
            self.successful_create_test_plan.json()["test_plan"]["is_current"], bool
        )
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["author"], self.author
        )
        self.assertIsInstance(
            self.successful_create_test_plan.json()["test_plan"]["author"], int
        )

    def test_create_test_plan_returns_200_with_only_title(self) -> None:
        """
        Тест-кейс, что метод добавления тест-плана возвращает 200
        и создает тест-план, если введен только заголовок.
        :return: None
        """
        self.successful_data = {
            "test_plan": {
                "title": self.title,
                "description": None,
                "author": None,
                "start_date": None,
                "end_date": None,
                "is_current": False
            }
        }
        self.successful_data_with_only_title = {
            "test_plan": {
                "title": self.title
            }
        }
        self.successful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.successful_create_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["title"], self.title)
        self.assertIsInstance(
            self.successful_create_test_plan.json()["test_plan"]["title"], str)
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["is_current"], False
        )
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["author"], None
        )

        self.successful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.successful_create_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["title"], self.title)
        self.assertIsInstance(
            self.successful_create_test_plan.json()["test_plan"]["title"], str)
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["is_current"], False
        )
        self.assertEqual(
            self.successful_create_test_plan.json()["test_plan"]["author"], None
        )

    def test_create_test_plan_returns_400_if_no_title(self) -> None:
        """
        Тест-кейс, что метод на создание тест-плана возвращает 400,
        если нет названия тест-плана.
        :return: None
        """
        self.unsuccessful_data: dict = {
            "test_plan": {
                "title": None,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["title"][0],
            "Title is required")

        self.unsuccessful_data_with_blank_title: dict = {
            "test_plan": {
                "title": "",
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_blank_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["title"][0],
            "Title is required")

        self.unsuccessful_data_with_only_title: dict = {
            "test_plan": {
                "title": "",
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["title"][0],
            "Title is required")

    def test_create_test_plan_returns_400_if_wrong_date_format(self) -> None:
        """
        Тест-кейс, что метод создания тест-плана возвращает 400,
        если неверный формат даты.
        :return: None
        """
        self.unsuccessful_data_with_wrong_start_date_format: dict = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": "26-08-2023 17:44:00",
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_wrong_start_date_format,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["start_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )

        self.unsuccessful_data_with_wrong_end_date_format: dict = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": "26-08-2023 17:44:00",
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_wrong_end_date_format,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["end_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )

        self.unsuccessful_data_with_wrong_start_and_end_date_format: dict = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": "26-08-2023 17:44:00",
                "end_date": "30-08-2023 17:44:00",
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_wrong_start_and_end_date_format,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["start_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["end_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )

    def test_create_test_plan_returns_400_if_end_date_less_than_start_date(self) -> None:
        """
        Тест-кейс, что метод добавления тест-плана возвращает 400,
        если дата конца тестирования меньше даты начала тестирования.
        :return: None
        """
        self.unsuccessful_data_less_end_date: dict = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.wrong_testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_less_end_date,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["error"][0],
            "Incorrect date"
        )

    def test_create_test_plan_returns_400_if_wrong_author(self) -> None:
        """
        Тест-кейс, что метод на создание тест-плана возвращает 400,
        если автора нет в БД или переданы неверные параметры
        :return: None
        """
        self.unsuccessful_data_no_author_in_database: dict = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": 100,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_no_author_in_database,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["error"][0],
            "No such author"
        )

        self.unsuccessful_data_incorrect_author: dict = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": 1.1,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_incorrect_author,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["author"][0],
            "A valid integer is required."
        )

        self.unsuccessful_data_inactive_author: dict = {
            "test_plan": {
                "title": self.title,
                "description": self.description,
                "author": 2,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_inactive_author,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["errors"]["error"][0],
            "No such author"
        )

    def test_create_test_plan_returns_403_if_unauthorized(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если пользователь не авторизован.
        :return: None
        """
        self.successful_data_with_only_title = {
            "test_plan": {
                "title": self.title
            }
        }
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            headers=self.headers_auth,
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 403)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["detail"],
            "Authentication credentials were not provided.")

    def test_create_test_plan_returns_403_if_token_expired(self) -> None:
        """
        Тест-кейс, что метод создания тест-плана возвращает 403,
        если JWT-токен просрочен.
        :return: None
        """
        self.successful_data_with_only_title = {
            "test_plan": {
                "title": self.title
            }
        }
        with open('./expired_token.txt', encoding='utf-8') as file:
            self.expired_token = file.read()
        self.unsuccessful_create_test_plan = requests.post(
            'http://127.0.0.1:8000/api/testplan/create/',
            auth=BearerAuth(token=self.expired_token),
            headers=self.headers_auth,
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_create_test_plan.status_code, 403)
        self.assertEqual(
            self.unsuccessful_create_test_plan.json()["test_plan"]["detail"],
            "Token has expired")
