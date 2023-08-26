"""
Модуль аутентификации с помощью JWT-токена
"""
import jwt
import typing
import datetime
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.request import Request

from .models import User


def _authenticate_credentials(request: Request, token: str) -> tuple:
    """
    Метод аутентификации токена
    :param request: Request
    :param token: str
    :return: Any
    """

    try:
        payload: typing.Mapping = jwt.decode(token, settings.SECRET_KEY)
    except Exception:
        msg: str = 'Token decode error'
        raise exceptions.AuthenticationFailed(msg)

    try:
        user: typing.Any = User.objects.get(pk=payload['UserId'])
    except User.DoesNotExist:
        msg: str = 'User not found'
        raise exceptions.AuthenticationFailed(msg)

    token_lifetime: datetime.datetime = datetime.datetime.strptime(
        str(payload["ExpirationDate"]), '%Y%m%d%H%M%S')
    time_difference: datetime.timedelta = token_lifetime - datetime.datetime.now()

    if int(time_difference.total_seconds()) <= 0:
        msg: str = 'Token has expired'
        raise exceptions.AuthenticationFailed(msg)

    if not user.is_active:
        msg: str = 'The user is inactive'
        raise exceptions.AuthenticationFailed(msg)

    return user, token


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Бэкенд с JWT-аутентификаицей
    """
    authentication_header_prefix: str = 'Bearer'

    SECONDS_IN_DAY: int = 2

    def authenticate(self, request: Request) -> typing.Any:
        """
        Метод аутентификации
        :param request: Request
        :return: None
        """
        request.user = None
        auth_header: list = authentication.get_authorization_header(request).split()
        auth_header_prefix: str = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        elif len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix: str = auth_header[0].decode("utf-8")
        token: str = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            return None

        return _authenticate_credentials(request, token)
