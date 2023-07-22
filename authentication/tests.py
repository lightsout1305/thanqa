"""
Тестирование приложения authentication
"""
from django.test import TestCase
from .models import User


class TestAuthModel(TestCase):
    """
    Тестирование модели User
    """
    # pylint: disable=attribute-defined-outside-init
    def setUp(self) -> None:
        """
        Создание тестовых данных для тестирования User
        :return: None
        """
        self.username: str = "test_user"
        self.email: str = "testuser@example.com"
        self.password: str = "test123!"
        self.first_name: str = "Иван"
        self.last_name: str = "Иванов"

    def test_create_ordinary_user(self) -> None:
        """
        Тест-кейс создания обычного пользователя.

        Проверка того, что у пользователя есть заданные тестовые данные:
        email, пароль, никнейм.

        Проверка типа данных полей пользователя.

        Проверка, что пользователь активен и не суперадмин.

        :return: None
        """
        self.user: User = User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name

        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.username, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)
        self.assertIsInstance(self.user.token, str)
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.token)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_super_user(self) -> None:
        """
        Тест-кейс создания суперадмина.

        Проверка того, что у пользователя есть заданные тестовые данные:
        email, пароль, никнейм.

        Проверка типа данных полей пользователя.

        Проверка, что пользователь активен и суперадмин.

        :return: None
        """
        self.superuser: User = User.objects.create_superuser(
            email=self.email,
            username=self.username,
            password=self.password
        )
        self.superuser.first_name = self.first_name
        self.superuser.last_name = self.last_name

        self.assertEqual(self.superuser.email, self.email)
        self.assertEqual(self.superuser.username, self.username)
        self.assertEqual(self.superuser.first_name, self.first_name)
        self.assertEqual(self.superuser.last_name, self.last_name)
        self.assertIsInstance(self.superuser.email, str)
        self.assertIsInstance(self.superuser.username, str)
        self.assertIsInstance(self.superuser.password, str)
        self.assertIsInstance(self.superuser.first_name, str)
        self.assertIsInstance(self.superuser.last_name, str)
        self.assertIsInstance(self.superuser.token, str)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.token, str)
