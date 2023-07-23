"""
Представления приложения api
"""
import typing
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import LoginSerializer
from .renderers import UserJSONRenderer


class LoginAPIView(APIView):
    """
    Представление API авторизации
    """
    permission_classes: typing.ClassVar[tuple] = (AllowAny,)
    renderer_classes: typing.ClassVar[tuple] = (UserJSONRenderer,)
    serializer_class: typing.Any = LoginSerializer

    def post(self, request: Request) -> Response:
        """
        POST-запрос авторизации
        :param request: Request
        :return: Response
        """
        user: typing.Any = request.data.get("user", {})
        serializer: LoginSerializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
