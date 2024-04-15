from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.enums.error_enum import ErrorEnum
from core.exception.email_exception import EmailException
from core.exception.export_file_exception import ExportFileException
from core.exception.jwt_exception import JwtException
from core.exception.order_permission_exception import OrderPermissionException
from core.exception.token_exception import CreateTokenException


def error_handler(exc: Exception, context: dict) -> Response:
    handlers = {
        'JwtException': _jwt_validation_error,
        'EmailException': _email_validation_error,
        'ExportFileException': _export_file_error,
        'TokenException': _token_create_error,
        'OrderPermissionException': _order_permission_error
    }
    response = exception_handler(exc, context)
    exc_class = exc.__class__.__name__
    if exc_class in handlers:
        return handlers[exc_class](exc, context)
    return response


def _jwt_validation_error(exc: JwtException, context: dict) -> Response:
    return Response(ErrorEnum.JWT.msg, ErrorEnum.JWT.code)


def _email_validation_error(exc: EmailException, context: dict) -> Response:
    return Response(ErrorEnum.EMAIL.msg, ErrorEnum.EMAIL.code)


def _export_file_error(exc: ExportFileException, context: dict) -> Response:
    return Response(ErrorEnum.EXPORT.msg, ErrorEnum.EXPORT.code)


def _token_create_error(exc: CreateTokenException, context: dict) -> Response:
    return Response(ErrorEnum.TOKEN.msg, ErrorEnum.TOKEN.code)


def _order_permission_error(exc: OrderPermissionException, context: dict) -> Response:
    return Response(ErrorEnum.ORDER_PERMISSION.msg, ErrorEnum.ORDER_PERMISSION.code)
