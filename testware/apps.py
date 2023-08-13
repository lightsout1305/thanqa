"""
Модуль конфигурации приложения testware
"""
from django.apps import AppConfig


class TestwareConfig(AppConfig):
    """
    Конфигурация приложения testware
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testware'
