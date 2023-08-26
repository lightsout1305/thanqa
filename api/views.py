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
from authentication.models import User


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
        test_plan_data: typing.Any = request.data.get("test_plan", {})

        try:
            description = test_plan_data["description"]
        except KeyError:
            description = None

        try:
            author = test_plan_data["author"]
        except KeyError:
            author = None

        try:
            start_date = test_plan_data["start_date"]
        except KeyError:
            start_date = None

        try:
            end_date = test_plan_data["end_date"]
        except KeyError:
            end_date = None

        try:
            is_current = test_plan_data["is_current"]
        except KeyError:
            is_current = False

        serializer: TestPlanSerializer = self.serializer_class(data=test_plan_data)
        if serializer.is_valid(raise_exception=True):
            test_plan: TestPlan = TestPlan.objects.create(
                title=test_plan_data["title"],
                description=description,
                author_id=author,
                is_current=is_current,
                start_date=start_date,
                end_date=end_date
            )
            test_plan.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
