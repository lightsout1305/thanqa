"""
Модуль настройки страницы администрирования приложения testware
"""
from django.contrib import admin
from .models import TestPlan


@admin.register(TestPlan)
class TestPlanAdmin(admin.ModelAdmin):
    """
    Регистрация модели TestPlan
    на странице администрирования
    """
    list_display = ['title', 'author', 'start_date', 'end_date']
    list_filter = ['title', 'author']
