"""
Представления приложения api.
Здесь собраны все API-представления проекта TestCasesTable.
"""
import typing

from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from authentication.models import User
from testware.models import TestPlan
from .serializers import LoginSerializer, CreateTestPlanSerializer, \
    UpdateTestPlanSerializer, DeleteTestPlanSerializer, GetTestPlansSerializer, GetUsersSerializer
from .renderers import LoginJSONRenderer, TestPlanJSONRenderer, UserJSONRenderer


class LoginAPIView(APIView):
    """
    Представление API авторизации
    """
    permission_classes: typing.ClassVar[tuple] = (AllowAny,)
    renderer_classes: typing.ClassVar[tuple] = (LoginJSONRenderer,)
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
            if is_current:
                test_plan.is_current = is_current
                test_plans = TestPlan.objects.exclude(
                    id=test_plan.id).filter(is_current=True, deleted=None)
                for obj in test_plans:
                    obj.is_current = False
                    obj.save()
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
            if is_current:
                test_plans = TestPlan.objects.exclude(
                    id=test_plan_data["test_plan_id"]).filter(
                    is_current=True,
                    deleted=None)
                for obj in test_plans:
                    obj.is_current = False
                    obj.save()
            test_plan.is_current = is_current
            test_plan.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteTestPlanApiView(APIView):
    """
    Метод удаления тест-плана
    """
    permission_classes: typing.ClassVar[tuple] = (IsAuthenticated,)
    renderer_classes: typing.ClassVar[tuple] = (TestPlanJSONRenderer,)
    serializer_class: typing.Any = DeleteTestPlanSerializer

    def delete(self, request: Request) -> Response:
        """
        DELETE-запрос удаления тест-плана
        :param request: Request
        :return: Response
        """
        test_plan_data: typing.Any = request.data.get("test_plan", {})
        serializer: DeleteTestPlanSerializer = self.serializer_class(data=test_plan_data)
        if serializer.is_valid(raise_exception=True):
            test_plan: TestPlan = TestPlan.objects.get(id=test_plan_data["test_plan_id"])
            test_plan.deleted = timezone.now()
            test_plan.is_current = False
            test_plan.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetTestPlanView(APIView):
    """
    Метод извлечения текущего тест-плана
    """
    permission_classes: typing.ClassVar[tuple] = (IsAuthenticated,)
    renderer_classes: typing.ClassVar[tuple] = (TestPlanJSONRenderer,)

    def get(self, request: Request) -> Response:
        """
        GET-запрос извлечения 1 тест-плана
        :param request: Request
        :return: Response
        """
        data: dict
        try:
            test_plan: TestPlan = TestPlan.objects.get(is_current=True, deleted=None)
            data = {
                "test_plan_id": test_plan.id,
                "title": test_plan.title,
                "description": test_plan.description,
                "start_date": test_plan.start_date.isoformat(),
                "end_date": test_plan.end_date.isoformat(),
                "author": test_plan.author.id,
                "is_current": test_plan.is_current
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except TestPlan.DoesNotExist:
            data = {
                "data": None
            }
            return Response(data=data, status=status.HTTP_200_OK)


class GetTestPlansAPIView(ListAPIView):
    """
    Метод извлечения всех тест-планов в алфавитном порядке
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GetTestPlansSerializer
    renderer_classes = (TestPlanJSONRenderer,)

    def get_queryset(self) -> QuerySet[TestPlan]:
        """
        Извлечение всех тест-планов
        :return:
        """
        queryset: QuerySet[TestPlan]
        title: typing.Any = self.request.query_params.get("title")
        if title is not None:
            queryset = TestPlan.objects.filter(
                deleted=None, title__icontains=title, is_current=False).order_by('id')
        else:
            queryset = TestPlan.objects.filter(deleted=None, is_current=False).order_by('id')
        return queryset


class GetUsersAPIView(ListAPIView):
    """
    Метод извлечения списка пользователей.

    Метод возвращает ID, имя, фамилию и email пользователя.

    Метод возвращает список, отсортированный по ID по возрастанию
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GetUsersSerializer
    renderer_classes = (UserJSONRenderer,)
    queryset = User.objects.filter(is_active=True, is_staff=True).order_by('id')
