"""
Модуль с моделями приложения authentication
"""
import typing
from datetime import datetime, timedelta
import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    Кастомный класс UserManager
    """

    def create_user(self, username: str, email: str,
                    password: str | None = None) -> typing.Any:
        """
        Создает и возвращает пользователя с username, email и password
        :param username: str
        :param email: str
        :param password: str
        :return: AbstractBaseUser
        """
        if username is None:
            raise TypeError("У пользователей должен быть никнейм")

        if email is None:
            raise TypeError("У пользователей должен быть email")
        user: typing.Any = self.model(
            username=username,
            email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None) -> typing.Any:
        """
        Создает и возвращает суперадминистратора
        :param username: str
        :param email: str
        :param password: str
        :return: BaseUserManager
        """
        if password is None:
            raise TypeError("У суперадминов должен быть пароль")

        user: typing.Any = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Таблица с пользователями
    """
    username: models.CharField = models.CharField(db_index=True, max_length=255, unique=True)
    first_name: models.CharField = models.CharField(blank=True)
    last_name: models.CharField = models.CharField(blank=True)
    email: models.EmailField = models.EmailField(db_index=True, unique=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    USERNAME_FIELD: typing.ClassVar[str] = "email"
    REQUIRED_FIELDS: typing.ClassVar[list] = ["username"]

    objects: UserManager = UserManager()

    def __str__(self) -> str:
        """
        Строковое представление модели User - email
        :return: str
        """
        return str(self.email)

    @property
    def token(self) -> str:
        """
        Вернуть токен пользователя
        :return: str
        """
        return self._generate_jwt_token()

    def get_full_name(self) -> str:
        """
        Вернуть имя и фамилию пользователя
        :return: str
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        """
        Вернуть никнейм пользователя
        :return: str
        """
        return str(self.username)

    def _generate_jwt_token(self) -> str:
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор
        пользователя.
        Срок действия токена - 1 день от даты создания.
        :return: str
        """
        expiration_date: datetime = datetime.now() + timedelta(days=1)

        token: bytes = jwt.encode({
            "UserId": self.pk,
            "ExpirationDate": int(expiration_date.strftime("%Y%m%d%H%M%S"))
        }, settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")
