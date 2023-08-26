"""
Модуль с тестами приложения testware
"""
import pytz
from django.test import TestCase
from django.utils import timezone
from authentication.models import User
from .models import TestPlan


class TestTestPlan(TestCase):
    """
    Тестирование таблицы TestPlan
    """
    # pylint: disable=attribute-defined-outside-init
    def setUp(self) -> None:
        """
        Инициализация тестовых данных
        :return: None
        """
        self.title: str = "Test"
        self.description: str = "Test description"
        self.author: User = User.objects.create(
            username='test_user',
            password='test123!',
            email='test-user@example.com'
        )
        self.testing_start_date: timezone.datetime = \
            timezone.datetime(2023, 8, 13, 10, 0, 53, tzinfo=pytz.UTC)
        self.testing_end_date: timezone.datetime = \
            timezone.datetime(2023, 8, 27, 10, 0, 53, tzinfo=pytz.UTC)
        self.is_current: bool = True
        self.test_plan: TestPlan

    def test_create_test_plan(self) -> None:
        """
        Тест-кейс, что тест-план успешно создан.

        Проверка того, что тест-план имеет следующие данные:
        1. Название (строка)
        2. Описание (строка)
        3. Автор (ID)
        4. Дата начала тестирования (дата в ISO-формате)
        5. Дата окончания тестирования (дата в ISO-формате)
        6. Тест-план текущий (булевое значение)

        :return: None
        """
        self.test_plan = TestPlan.objects.create(
            title=self.title,
            description=self.description,
            author=self.author,
            start_date=self.testing_start_date,
            end_date=self.testing_end_date,
            is_current=self.is_current
        )

        # Проверка названия тест-плана
        self.assertEqual(self.test_plan.title, self.title)
        self.assertIsInstance(self.test_plan.title, str)

        # Проверка описания тест-плана
        self.assertEqual(self.test_plan.description, self.description)
        self.assertIsInstance(self.test_plan.description, str)

        # Проверка автора тест-плана
        self.assertEqual(self.test_plan.author, self.author)
        self.assertIsInstance(self.test_plan.author, User)

        # Проверка даты начала тестирования тест-плана
        self.assertEqual(
            self.test_plan.start_date, self.testing_start_date)
        self.assertIsInstance(
            self.test_plan.start_date, timezone.datetime)

        # Проверка даты окончания тестирования тест-плана
        self.assertEqual(
            self.test_plan.end_date, self.testing_end_date)
        self.assertIsInstance(
            self.test_plan.end_date, timezone.datetime)

        # Проверка поля текущего тест-плана
        self.assertEqual(self.test_plan.is_current, self.is_current)
        self.assertIsInstance(self.test_plan.is_current, bool)

    def test_create_test_plan_with_only_necessary_fields(self) -> None:
        """
        Тест-кейс, что создан тест-план с обязательными полями.

        Проверка полей:
        1. Название (строка)

        :return: None
        """
        self.test_plan = TestPlan.objects.create(
            title=self.title
        )

        # Проверка названия тест-плана
        self.assertEqual(self.test_plan.title, self.title)
        self.assertIsInstance(self.test_plan.title, str)

        # Проверка описания тест-плана
        self.assertEqual(self.test_plan.description, None)

        # Проверка автора тест-плана
        self.assertEqual(self.test_plan.author, None)

        # Проверка даты начала тестирования тест-плана
        self.assertEqual(self.test_plan.start_date, None)

        # Проверка даты окончания тестирования тест-плана
        self.assertEqual(self.test_plan.end_date, None)

        # Проверка поля текущего тест-плана
        self.assertEqual(self.test_plan.is_current, False)
