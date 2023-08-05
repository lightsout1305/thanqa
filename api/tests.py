"""
Модуль с тестами приложения api
"""
import requests
import environ
from django.test import TestCase
from requests import Response
from thanqa_tms.settings import BASE_DIR


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
