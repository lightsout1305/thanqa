"""
Модуль с исключениями api
"""
import typing
from rest_framework.response import Response
from rest_framework.views import exception_handler


def core_exception_handler(exc: typing.Any,
                           context: typing.Any) -> Response | None:
    """
    Обработчик исключений в API.
    Если возникает исключение, которые мы не обрабатываем здесь явно, мы
    хотим передать его обработчику исключений по-умолчанию, предлагаемому
    DRF. И все же, если мы обрабатываем такой тип исключения, нам нужен
    доступ к сгенерированному DRF - получим его заранее здесь.
    :param exc: Any
    :param context: Any
    :return: Response | None
    """
    response: Response = exception_handler(exc, context)
    handlers: dict = {
        "ValidationError": _handle_generic_error
    }

    exception_class: str = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc: typing.Any, context: typing.Any,
                          response: typing.Any) -> Response:
    # pylint:disable=unused-argument
    """
    Это самый простой обработчик исключений, который мы можем создать. Мы
    берем ответ сгенерированный DRF и заключаем его в ключ 'errors'.
    :param exc: Any
    :param context: Any
    :param response: Response | None
    :return: Response
    """
    response.data = {
        "errors": response.data
    }

    return response
