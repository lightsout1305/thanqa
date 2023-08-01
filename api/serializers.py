"""
Сериализаиия методов приложения api
"""
import typing
from rest_framework import serializers
from django.contrib.auth import authenticate
from authentication.models import User


class LoginSerializer(serializers.Serializer):
    """
    Сериализация метода Login
    """
    email: serializers.CharField = \
        serializers.CharField(
            max_length=255, error_messages={"null": "Enter your E-mail",
                                            "blank": "Enter your E-mail"})
    username: serializers.CharField = serializers.CharField(max_length=255,
                                                            read_only=True)
    password: serializers.CharField = \
        serializers.CharField(
            max_length=128,
            write_only=True,
            error_messages={"null": "Enter your password",
                            "blank": "Enter your password"})
    token: serializers.CharField = serializers.CharField(
        max_length=255,
        read_only=True)

    def validate(self, attrs: typing.Any) -> dict:
        """
        Валидация введенных данных авторизации
        :param attrs: dict
        :return: dict
        """
        email: str = attrs.get("email")
        password: str = attrs.get("password")

        user: User = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "Invalid login or password"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User is inactive"
            )

        return {
            "email": user.email,
            "username": user.username,
            "token": user.token
        }

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
