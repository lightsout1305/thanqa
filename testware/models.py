"""
Модуль с таблицами тест-кейса, тестового прогона, чеклиста и тестового плана
"""
from django.db import models
from django.urls import reverse
from authentication.models import User


class TestPlan(models.Model):
    """
    Таблица с тест-планами
    """
    title: models.CharField = models.CharField(
        max_length=150
    )
    description: models.TextField = models.TextField(
        blank=True, null=True
    )
    author: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE,
        blank=True, null=True
    )
    start_date: models.DateTimeField = models.DateTimeField(
        blank=True, null=True
    )
    end_date: models.DateTimeField = models.DateTimeField(
        blank=True, null=True
    )
    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    modified: models.DateTimeField = models.DateTimeField(
        auto_now=True
    )
    deleted: models.DateTimeField = models.DateTimeField(
        blank=True, null=True
    )
    is_current: models.BooleanField = models.BooleanField(
        default=False
    )

    def __str__(self) -> str:
        """
        Возвращение строкового представления тест-плана
        :return: str
        """
        return str(self.title)

    def get_absolute_url(self) -> str:
        """
        Возвращение одного тест-плана по ID
        :return: str
        """
        return reverse("test_plan_info", args=[self.id])
