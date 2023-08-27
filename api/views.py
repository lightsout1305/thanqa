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

from authentication.models import User
from testware.models import TestPlan
from .serializers import LoginSerializer, CreateTestPlanSerializer, UpdateTestPlanSerializer
from .renderers import UserJSONRenderer, TestPlanJSONRenderer


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
    serializer_class: typing.Any = CreateTestPlanSerializer

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

        serializer: CreateTestPlanSerializer = self.serializer_class(data=test_plan_data)
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
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateTestPlanApiView(APIView):
    """
    Метод на редактирование тест-плана
    """
    permission_classes: typing.ClassVar[tuple] = (IsAuthenticated,)
    renderer_classes: typing.ClassVar[tuple] = (TestPlanJSONRenderer,)
    serializer_class: typing.Any = UpdateTestPlanSerializer

    def put(self, request: Request) -> Response:
        """
        PUT-запрос редактирования тест-плана
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

        serializer: UpdateTestPlanSerializer = self.serializer_class(data=test_plan_data)
        if serializer.is_valid(raise_exception=True):
            test_plan: TestPlan = TestPlan.objects.get(id=test_plan_data["test_plan_id"])
            test_plan.title = test_plan_data["title"]
            test_plan.description = description
            test_plan.start_date = start_date
            test_plan.end_date = end_date
            test_plan.author = User.objects.get(id=author) if author else None
            test_plan.is_current = is_current
            test_plan.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
