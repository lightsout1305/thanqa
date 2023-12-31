"""
Сериализаиия методов приложения api
"""
import typing

from django.contrib.auth import authenticate
from rest_framework import serializers
from authentication.models import User
from testware.models import TestPlan


class LoginSerializer(serializers.Serializer):
    """
    Сериализация метода Login
    """
    email: serializers.CharField = \
        serializers.CharField(
            max_length=255,
            error_messages={"null": "Enter your E-mail",
                            "blank": "Enter your E-mail"})
    username: serializers.CharField = serializers.CharField(
        max_length=255,
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

    def create(self, validated_data) -> typing.Any:
        pass

    def update(self, instance, validated_data) -> typing.Any:
        pass


class CreateTestPlanSerializer(serializers.Serializer):
    """
    Сериализация методов тест-плана
    """
    title: serializers.CharField = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={"blank": "Title is required",
                        "null": "Title is required"}
    )
    description: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        write_only=True
    )
    is_current: serializers.BooleanField = serializers.BooleanField(
        required=False,
        default=False
    )
    start_date: serializers.DateTimeField = serializers.DateTimeField(
        required=False,
        allow_null=True,
        write_only=True
    )
    end_date: serializers.DateTimeField = serializers.DateTimeField(
        required=False,
        allow_null=True,
        write_only=True
    )
    author: serializers.IntegerField = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    def validate(self, attrs: typing.Any) -> dict:
        """
        Валидация данных тест-плана
        :param attrs: Any
        :return: dict
        """
        title: str = attrs.get("title")
        author: int = attrs.get("author")
        is_current: bool = attrs.get("is_current")
        active_authors: typing.Any = \
            list(User.objects.filter(is_active=True).values_list('id', flat=True))

        if author is not None:
            if author not in active_authors:
                raise serializers.ValidationError(
                    "No such author"
                )

        try:
            if attrs['start_date'] is not None and attrs['end_date'] is not None:
                if attrs['start_date'] > attrs['end_date']:
                    raise serializers.ValidationError(
                        "Incorrect date"
                    )
        except KeyError:
            pass

        return {
            "title": title,
            "author": author,
            "is_current": is_current
        }

    def create(self, validated_data) -> typing.Any:
        pass

    def update(self, instance, validated_data) -> typing.Any:
        pass


class UpdateTestPlanSerializer(serializers.Serializer):
    """
    Сериализация методов тест-плана
    """
    test_plan_id: serializers.IntegerField = serializers.IntegerField(
        required=True,
        error_messages={"blank": "ID is required",
                        "null": "ID is required"}
    )
    title: serializers.CharField = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={"blank": "Title is required",
                        "null": "Title is required"}
    )
    description: serializers.CharField = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        write_only=True
    )
    is_current: serializers.BooleanField = serializers.BooleanField(
        required=False,
        default=False
    )
    start_date: serializers.DateTimeField = serializers.DateTimeField(
        required=False,
        allow_null=True,
        write_only=True
    )
    end_date: serializers.DateTimeField = serializers.DateTimeField(
        required=False,
        allow_null=True,
        write_only=True
    )
    author: serializers.IntegerField = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    def validate(self, attrs: typing.Any) -> dict:
        """
        Валидация данных тест-плана
        :param attrs: Any
        :return: dict
        """
        test_plan_id = attrs.get("test_plan_id")
        title: str = attrs.get("title")
        author: int = attrs.get("author")
        is_current: bool = attrs.get("is_current")
        active_authors: typing.Any = \
            list(User.objects.filter(is_active=True).values_list('id', flat=True))
        test_plans: typing.Any = \
            list(TestPlan.objects.filter(deleted=None).values_list('id', flat=True))

        if test_plan_id not in test_plans:
            raise serializers.ValidationError(
                "No such test plan"
            )

        if author is not None:
            if author not in active_authors:
                raise serializers.ValidationError(
                    "No such author"
                )

        try:
            if attrs['start_date'] is not None and attrs['end_date'] is not None:
                if attrs['start_date'] > attrs['end_date']:
                    raise serializers.ValidationError(
                        "Incorrect date"
                    )
        except KeyError:
            pass

        return {
            "test_plan_id": test_plan_id,
            "title": title,
            "author": author,
            "is_current": is_current
        }

    def create(self, validated_data) -> typing.Any:
        pass

    def update(self, instance, validated_data) -> typing.Any:
        pass


class DeleteTestPlanSerializer(serializers.Serializer):
    """
    Сериализация метода удаления тест-плана
    """
    test_plan_id: serializers.IntegerField = serializers.IntegerField(
        required=True,
        error_messages={"blank": "ID is required",
                        "null": "ID is required"}
    )

    def validate(self, attrs: typing.Any) -> dict:
        """
        Валидация данных для удаления тест-плана
        :param attrs: Any
        :return: dict
        """
        test_plan_id: int = attrs.get("test_plan_id")
        test_plans: typing.Any = \
            list(TestPlan.objects.filter(deleted=None).values_list('id', flat=True))

        if test_plan_id not in test_plans:
            raise serializers.ValidationError(
                "No such test plan"
            )

        return {
            "test_plan_id": test_plan_id
        }

    def create(self, validated_data) -> typing.Any:
        pass

    def update(self, instance, validated_data) -> typing.Any:
        pass


class GetTestPlansSerializer(serializers.ModelSerializer):
    """
    Сериализация метода GetTestPlans
    """

    class Meta:
        model = TestPlan
        exclude = ('created', 'modified', 'deleted',)


class GetUsersSerializer(serializers.ModelSerializer):
    """
    Сериализация метода GetUsers
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
