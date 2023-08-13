"""
Модуль настройки страницы администрирования приложения authentication
"""
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Регистрация модели User
    на странице администрирования
    """
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['username', 'email']
