"""
Модуль с рендером JSON для приложения api
"""
import json
import typing
from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    """
    Рендер JSON для модели User
    """
    charset: str = "utf-8"

    def render(
            self,
            data: typing.Any,
            accepted_media_type: typing.Any = None,
            renderer_context: typing.Any = None) -> str:
        """
        Функция рендера JSON модели User
        :param data: Any
        :param accepted_media_type: Any
        :param renderer_context: Any
        :return: str
        """
        errors: typing.Any = data.get("errors", None)
        token: typing.Any = data.get("token", None)

        if errors is not None:
            JSONRenderer.render(self, data)

        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode(encoding="utf-8")

        return json.dumps({
            "user": data
        })


class TestPlanJSONRenderer(JSONRenderer):
    """
    Рендер JSON для модели тест-плана
    """
    charset: str = "utf-8"

    def render(
            self,
            data: typing.Any,
            accepted_media_type: typing.Any = None,
            renderer_context: typing.Any = None) -> str:
        """
        Функция-рендер для модели TestPlan
        :param data: Any
        :param accepted_media_type: Any
        :param renderer_context: Any
        :return: str
        """
        errors = data.get("errors", None) if isinstance(data, dict) else data

        if errors is not None:
            JSONRenderer.render(self, data)

        return json.dumps({
            "test_plan": data
        })
