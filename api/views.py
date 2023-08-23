"""
Представления приложения api.
Здесь собраны все API-представления проекта ThanQA.
"""
import typing
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import LoginSerializer, TestPlanSerializer
from .renderers import UserJSONRenderer, TestPlanJSONRenderer

from testware.models import TestPlan


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
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateTestPlanAPIView(APIView):
    """
    Представление API создания тест-плана
    """
    permission_classes: typing.ClassVar[tuple] = (IsAuthenticated,)
    renderer_classes: typing.ClassVar[tuple] = (TestPlanJSONRenderer,)
    serializer_class: typing.Any = TestPlanSerializer

    def post(self, request: Request) -> Response:
        """
        POST-запрос создания тест-плана
        :param request: Request
        :return: Response
        """
        test_plan: typing.Any = request.data.get("test_plan", {})
        serializer: TestPlanSerializer = self.serializer_class(data=test_plan)
        if serializer.is_valid(raise_exception=True):
            tp: TestPlan = TestPlan.objects.create(
                title=test_plan["title"],
                description=test_plan["description"],
                author_id=test_plan["author"],
                is_current=test_plan["is_current"],
                start_date=test_plan["start_date"],
                end_date=test_plan["end_date"]
            )
            tp.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
