"""
Модуль с тестами приложения api
"""
import requests
import environ
from django.test import TestCase
from requests import Response
from requests.auth import AuthBase
from thanqa_tms.settings import BASE_DIR
from testware.models import TestPlan


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

    # pylint: disable=too-many-lines

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
            self.expired_token: str = file.read()
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


class TestUpdateTestPlan(TestCase):
    """
    Тестирование метода UpdateTestPlan
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
        self.test_plan_id: int | float = 100
        self.title: str = "Релиз-план 2023.17 по функционалу добавления/редактирования" \
                          "/прочтения/удаления тест-плана"
        with open('./description_for_test_plan.txt', encoding='utf-8') as file:
            self.description = file.read()
        self.author: int = 1
        self.is_current: bool = False
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
        self.unsuccessful_data: dict
        self.successful_update_test_plan: Response
        self.successful_data_with_only_title: dict
        self.unsuccessful_update_test_plan: Response

    def test_update_test_plan_returns_200(self) -> None:
        """
        Тест-кейс, что метод редактирования тест-плана возвращает 200
        и редактирует тест-план, если все поля введены.
        :return: None
        """
        self.successful_data = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.successful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.successful_data,
            timeout=10
        )
        self.assertEqual(self.successful_update_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["title"], self.title)
        self.assertIsInstance(
            self.successful_update_test_plan.json()["test_plan"]["title"], str)
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["is_current"], self.is_current
        )
        self.assertIsInstance(
            self.successful_update_test_plan.json()["test_plan"]["is_current"], bool
        )
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["author"], self.author
        )
        self.assertIsInstance(
            self.successful_update_test_plan.json()["test_plan"]["author"], int
        )

    def test_update_test_plan_returns_200_with_only_title(self) -> None:
        """
        Тест-кейс, что метод редактирования тест-плана возвращает 200
        и редактирует тест-план, если введен только заголовок.
        :return: None
        """
        self.successful_data = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
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
                "test_plan_id": self.test_plan_id,
                "title": self.title
            }
        }
        self.successful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.successful_update_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["title"], self.title)
        self.assertIsInstance(
            self.successful_update_test_plan.json()["test_plan"]["title"], str)
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["is_current"], False
        )
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["author"], None
        )

        self.successful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.successful_update_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["title"], self.title)
        self.assertIsInstance(
            self.successful_update_test_plan.json()["test_plan"]["title"], str)
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["is_current"], False
        )
        self.assertEqual(
            self.successful_update_test_plan.json()["test_plan"]["author"], None
        )

    def test_update_test_plan_returns_400_if_no_id(self) -> None:
        """
        Тест-кейс, что метод редактирования тест-плана возвращает 400,
        если не указан ID.
        :return: None
        """
        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": None,
                "title": self.title,
                "description": None,
                "author": None,
                "start_date": None,
                "end_date": None,
                "is_current": False
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["test_plan_id"][0],
            "ID is required")

        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": "",
                "title": self.title,
                "description": None,
                "author": None,
                "start_date": None,
                "end_date": None,
                "is_current": False
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["test_plan_id"][0],
            "A valid integer is required.")

        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": 1.1,
                "title": self.title,
                "description": None,
                "author": None,
                "start_date": None,
                "end_date": None,
                "is_current": False
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["test_plan_id"][0],
            "A valid integer is required.")

        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": 0,
                "title": self.title,
                "description": None,
                "author": None,
                "start_date": None,
                "end_date": None,
                "is_current": False
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["error"][0],
            "No such test plan")

    def test_update_test_plan_returns_400_if_no_title(self) -> None:
        """
        Тест-кейс, что метод на редактирование тест-плана возвращает 400,
        если нет названия тест-плана.
        :return: None
        """
        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": None,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["title"][0],
            "Title is required")

        self.unsuccessful_data_with_blank_title: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": "",
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_blank_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["title"][0],
            "Title is required")

        self.unsuccessful_data_with_only_title: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": "",
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["title"][0],
            "Title is required")

    def test_update_test_plan_returns_400_if_wrong_date_format(self) -> None:
        """
        Тест-кейс, что метод редактирования тест-плана возвращает 400,
        если неверный формат даты.
        :return: None
        """
        self.unsuccessful_data_with_wrong_start_date_format: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": "26-08-2023 17:44:00",
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_wrong_start_date_format,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["start_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )

        self.unsuccessful_data_with_wrong_end_date_format: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": "26-08-2023 17:44:00",
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_wrong_end_date_format,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["end_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )

        self.unsuccessful_data_with_wrong_start_and_end_date_format: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": "26-08-2023 17:44:00",
                "end_date": "30-08-2023 17:44:00",
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_with_wrong_start_and_end_date_format,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["start_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["end_date"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        )

    def test_update_test_plan_returns_400_if_end_date_less_than_start_date(self) -> None:
        """
        Тест-кейс, что метод редактирования тест-плана возвращает 400,
        если дата конца тестирования меньше даты начала тестирования.
        :return: None
        """
        self.unsuccessful_data_less_end_date: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": self.author,
                "start_date": self.testing_start_date,
                "end_date": self.wrong_testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_less_end_date,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["error"][0],
            "Incorrect date"
        )

    def test_update_test_plan_returns_400_if_wrong_author(self) -> None:
        """
        Тест-кейс, что метод на редактирование тест-плана возвращает 400,
        если автора нет в БД или переданы неверные параметры
        :return: None
        """
        self.unsuccessful_data_no_author_in_database: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": 100,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_no_author_in_database,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["error"][0],
            "No such author"
        )

        self.unsuccessful_data_incorrect_author: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": 1.1,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_incorrect_author,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["author"][0],
            "A valid integer is required."
        )

        self.unsuccessful_data_inactive_author: dict = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title,
                "description": self.description,
                "author": 2,
                "start_date": self.testing_start_date,
                "end_date": self.testing_end_date,
                "is_current": self.is_current
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data_inactive_author,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["errors"]["error"][0],
            "No such author"
        )

    def test_update_test_plan_returns_403_if_unauthorized(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если пользователь не авторизован.
        :return: None
        """
        self.successful_data_with_only_title = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title
            }
        }
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            headers=self.headers_auth,
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 403)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["detail"],
            "Authentication credentials were not provided.")

    def test_update_test_plan_returns_403_if_token_expired(self) -> None:
        """
        Тест-кейс, что метод редактирования тест-плана возвращает 403,
        если JWT-токен просрочен.
        :return: None
        """
        self.successful_data_with_only_title = {
            "test_plan": {
                "test_plan_id": self.test_plan_id,
                "title": self.title
            }
        }
        with open('./expired_token.txt', encoding='utf-8') as file:
            self.expired_token = file.read()
        self.unsuccessful_update_test_plan = requests.put(
            'http://127.0.0.1:8000/api/testplan/update/',
            auth=BearerAuth(token=self.expired_token),
            headers=self.headers_auth,
            json=self.successful_data_with_only_title,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_update_test_plan.status_code, 403)
        self.assertEqual(
            self.unsuccessful_update_test_plan.json()["test_plan"]["detail"],
            "Token has expired")


class TestDeleteTestPlan(TestCase):
    """
    Тестирование метода удаления тест-плана
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
        self.test_plan_id: int
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
        self.unsuccessful_data: dict
        self.successful_delete_test_plan: Response
        self.unsuccessful_delete_test_plan: Response

    def test_delete_test_plan_returns_200(self) -> None:
        """
        Тест-кейс, что метод удаления тест-плана возвращает 200,
        если тест-план есть в БД и он не удален.
        :return: None
        """
        self.test_plan_id = int(input("Enter test plan ID for deletion: "))
        self.successful_data = {
            "test_plan": {
                "test_plan_id": self.test_plan_id
            }
        }
        self.successful_delete_test_plan = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.successful_data,
            timeout=10
        )
        self.assertEqual(self.successful_delete_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_delete_test_plan.json()["test_plan"]["test_plan_id"], self.test_plan_id)

    def test_delete_test_plan_returns_400_if_test_plan_already_deleted(self) -> None:
        """
        Тест-кейс, что метод возвращает 400, если тест-план уже удален.
        :return: None
        """
        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": 15
            }
        }
        self.unsuccessful_delete_test_plan = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_delete_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_delete_test_plan.json()["test_plan"]["errors"]["error"][0],
            "No such test plan")

    def test_delete_test_plan_returns_400_if_test_plan_not_found(self) -> None:
        """
        Тест-кейс, что метод возвращает 400, если тест-плана нет в БД
        :return: None
        """
        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": 0
            }
        }
        self.unsuccessful_delete_test_plan = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_delete_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_delete_test_plan.json()["test_plan"]["errors"]["error"][0],
            "No such test plan")

    def test_delete_test_plan_returns_400_if_no_id(self) -> None:
        """
        Тест-кейс, что метод удаления тест-плана возвращает 400,
        если не указан ID тест-плана.
        :return: None
        """
        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": None
            }
        }
        self.unsuccessful_delete_test_plan = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_delete_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_delete_test_plan.json()["test_plan"]["errors"]["test_plan_id"][0],
            "ID is required")

        self.unsuccessful_data = {
            "test_plan": {
                "test_plan_id": ""
            }
        }
        self.unsuccessful_delete_test_plan = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            json=self.unsuccessful_data,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_delete_test_plan.status_code, 400)
        self.assertEqual(
            self.unsuccessful_delete_test_plan.json()["test_plan"]["errors"]["test_plan_id"][0],
            "A valid integer is required.")

    def test_delete_test_plan_returns_403_if_unauthorized(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если пользователь не авторизован.
        :return: None
        """
        self.successful_data = {
            "test_plan": {
                "test_plan_id": 10
            }
        }
        self.successful_delete_test_plan = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            json=self.successful_data,
            timeout=10
        )
        self.assertEqual(self.successful_delete_test_plan.status_code, 403)
        self.assertEqual(
            self.successful_delete_test_plan.json()["test_plan"]["detail"],
            "Authentication credentials were not provided.")

    def test_delete_test_plan_returns_403_if_token_expired(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если токен просрочен.
        :return: None
        """
        with open('./expired_token.txt', encoding='utf-8') as file:
            self.expired_token = file.read()
        self.successful_data = {
            "test_plan": {
                "test_plan_id": 2
            }
        }
        self.successful_delete_test_plan = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.expired_token),
            json=self.successful_data,
            timeout=10
        )
        self.assertEqual(self.successful_delete_test_plan.status_code, 403)
        self.assertEqual(
            self.successful_delete_test_plan.json()["test_plan"]["detail"],
            "Token has expired")


class TestGetCurrentTestPlan(TestCase):
    """
    Тестирование метода GetCurrentTestPlan
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
        self.successful_get_current_test_plan: Response
        self.test_plan_id: int | float = 100
        self.title: str = "Релиз-план 2023.16 по функционалу добавления/редактирования" \
                          "/прочтения/удаления тест-плана"
        with open('./description_for_test_plan.txt', encoding='utf-8') as file:
            self.description = file.read()
        self.author: int = 1
        self.is_current: bool = True
        self.testing_start_date: str = "2023-08-23T20:38:43.469088Z"
        self.testing_end_date: str = "2023-08-30T20:38:43.469088Z"
        self.wrong_testing_end_date: str = "2023-07-30T20:38:43.469088Z"

    def test_get_current_test_plan_returns_200(self) -> None:
        """
        Тест-кейс, что метод текущего тест-плана возвращает 200,
        с тест-планом.
        :return: None
        """
        self.successful_get_current_test_plan = requests.get(
            "http://127.0.0.1:8000/api/testplan/current/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            timeout=10
        )
        self.assertEqual(self.successful_get_current_test_plan.status_code, 200)
        self.assertEqual(
            self.successful_get_current_test_plan.json()["test_plan"]["title"], self.title)
        self.assertEqual(
            self.successful_get_current_test_plan.json()["test_plan"]["description"],
            self.description
        )
        self.assertEqual(
            self.successful_get_current_test_plan.json()["test_plan"]["is_current"],
            self.is_current
        )
        self.assertEqual(
            self.successful_get_current_test_plan.json()["test_plan"]["author"], self.author
        )

    def test_get_current_test_plan_returns_200_if_no_test_plan(self) -> None:
        """
        Тест-кейс, что метод возвращения текущего тест-плана возвращает пустую
        информацию
        :return: None
        """
        self.current_test_plan_id: int = requests.get(
            "http://127.0.0.1:8000/api/testplan/current/",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.token),
            timeout=10
        ).json()["test_plan"]["test_plan_id"]
        self.successful_data = {
            "test_plan": {
                "test_plan_id": self.current_test_plan_id
            }
        }
        self.delete_test_plan: Response = requests.delete(
            "http://127.0.0.1:8000/api/testplan/delete/",
            auth=BearerAuth(token=self.token),
            headers=self.headers_auth,
            json=self.successful_data,
            timeout=10
        )
        self.successful_get_current_test_plan = requests.get(
            "http://127.0.0.1:8000/api/testplan/current/",
            auth=BearerAuth(token=self.token),
            headers=self.headers_auth,
            timeout=10
        )
        self.assertEqual(self.successful_get_current_test_plan.status_code, 200)
        self.assertIsNone(self.successful_get_current_test_plan.json()["test_plan"]["data"])

    def test_get_current_test_plan_returns_403_if_unauthorized(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если пользователь не авторизован.
        :return: None
        """
        self.successful_get_current_test_plan = requests.get(
            "http://127.0.0.1:8000/api/testplan/current",
            headers=self.headers_auth,
            timeout=10
        )
        self.assertEqual(self.successful_get_current_test_plan.status_code, 403)
        self.assertEqual(
            self.successful_get_current_test_plan.json()["test_plan"]["detail"],
            "Authentication credentials were not provided."
        )

    def test_get_current_test_plan_returns_403_if_token_expired(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если токен просрочен.
        :return: None
        """
        with open('./expired_token.txt', encoding='utf-8') as file:
            self.expired_token: str = file.read()
        self.successful_get_current_test_plan = requests.get(
            "http://127.0.0.1:8000/api/testplan/current",
            headers=self.headers_auth,
            auth=BearerAuth(token=self.expired_token),
            timeout=10
        )
        self.assertEqual(self.successful_get_current_test_plan.status_code, 403)
        self.assertEqual(
            self.successful_get_current_test_plan.json()["test_plan"]["detail"],
            "Token has expired")


class TestGetTestPlans(TestCase):
    """
    Тестирование метода GetTestPlans
    """

    env: environ.Env = environ.Env()
    env.read_env(BASE_DIR, ".env")

    count_from_db: int = TestPlan.objects.filter(deleted=None, is_current=False).count()

    # pylint: disable=too-many-lines
    # pylint: disable=attribute-defined-outside-init

    def setUp(self) -> None:
        """
        Инициализация тестовых данных
        :return: None
        """
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
        self.successful_get_test_plans: Response
        self.unsuccessful_get_test_plans: Response

    def test_get_test_plans_returns_200(self) -> None:
        """
        Тест-кейс, что метод возвращения тест-планов возвращает 200
        со всеми тест-планами
        :return: None
        """
        count_from_api: int = 0
        self.successful_get_test_plans = requests.get(
            "http://127.0.0.1:8000/api/testplan/all/",
            auth=BearerAuth(token=self.token),
            headers=self.headers_auth,
            timeout=10
        )

        try:
            while True:
                _ = self.successful_get_test_plans.json()["test_plan"][count_from_api]
                count_from_api += 1
        except IndexError:
            count_from_api -= 1
        self.assertEqual(self.successful_get_test_plans.status_code, 200)
        self.assertEqual(self.count_from_db, count_from_api)

    def test_get_test_plans_returns_ordered_objects(self) -> None:
        """
        Тест-кейс, что метод возвращения тест-плана возвращает отсортированный по ID список
        :return: None
        """
        self.successful_get_test_plans = requests.get(
            "http://127.0.0.1:8000/api/testplan/all/",
            auth=BearerAuth(token=self.token),
            headers=self.headers_auth,
            timeout=10
        )

        for i in range(1, self.count_from_db):
            current_id: int = self.successful_get_test_plans.json()["test_plan"][i]["id"]
            previous_id: int = self.successful_get_test_plans.json()['test_plan'][i - 1]["id"]
            if current_id <= previous_id:
                raise ValueError("Некорректная сортировка по ID")

    def test_get_test_plans_returns_search_results(self) -> None:
        """
        Тест-кейс, что метод возвращения тест-планов находит тест-план
        по строке поиска
        :return: None
        """
        count_from_api: int = 0
        self.successful_get_test_plans = requests.get(
            "http://127.0.0.1:8000/api/testplan/all?title=this",
            auth=BearerAuth(token=self.token),
            headers=self.headers_auth,
            timeout=10
        )
        try:
            while True:
                _ = self.successful_get_test_plans.json()["test_plan"][count_from_api]
                count_from_api += 1
                self.assertRegex(
                    self.successful_get_test_plans.json()['test_plan'][count_from_api]['title'],
                    "(?i)this")
        except IndexError:
            count_from_api -= 1

        for i in range(1, count_from_api):
            current_id: int = self.successful_get_test_plans.json()["test_plan"][i]["id"]
            previous_id: int = self.successful_get_test_plans.json()['test_plan'][i - 1]["id"]
            if current_id <= previous_id:
                raise ValueError("Некорректная сортировка по ID")

    def test_get_test_plans_returns_200_if_no_data_found(self) -> None:
        """
        Тест-кейс, что метод возвращения тест-планов возвращает пустой массив
        :return: None
        """
        self.successful_get_test_plans = requests.get(
            "http://127.0.0.1:8000/api/testplan/all?title=lol",
            auth=BearerAuth(token=self.token),
            headers=self.headers_auth,
            timeout=10
        )
        self.assertEqual(self.successful_get_test_plans.status_code, 200)
        self.assertFalse(self.successful_get_test_plans.json()['test_plan'])

    def test_get_test_plans_returns_403_if_unauthorized(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если пользователь неавторизован
        :return: None
        """
        self.unsuccessful_get_test_plans = requests.get(
            "http://127.0.0.1:8000/api/testplan/all/",
            headers=self.headers_auth,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_get_test_plans.status_code, 403)
        self.assertEqual(
            self.unsuccessful_get_test_plans.json()["test_plan"]["detail"],
            "Authentication credentials were not provided."
        )

    def test_get_test_plans_returns_403_if_expired_token(self) -> None:
        """
        Тест-кейс, что метод возвращает 403, если токен просрочен
        :return: None
        """
        with open('./expired_token.txt', encoding='utf-8') as file:
            self.expired_token: str = file.read()
        self.unsuccessful_get_test_plans = requests.get(
            "http://127.0.0.1:8000/api/testplan/all/",
            auth=BearerAuth(token=self.expired_token),
            headers=self.headers_auth,
            timeout=10
        )
        self.assertEqual(self.unsuccessful_get_test_plans.status_code, 403)
        self.assertEqual(
            self.unsuccessful_get_test_plans.json()["test_plan"]["detail"],
            "Token has expired"
        )
