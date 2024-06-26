from enum import Enum

from rest_framework import status


class ErrorEnum(Enum):
    JWT = (
        {'detail': 'Token invalid or expired'},
        status.HTTP_403_FORBIDDEN
    )
    EMAIL = (
        {'detail': 'Connection locked!'},
        status.HTTP_423_LOCKED
    )
    EXPORT = (
        {'detail': 'Export file failed!'},
        status.HTTP_503_SERVICE_UNAVAILABLE
    )
    TOKEN = (
        {'detail': 'Create token failed!'},
        status.HTTP_503_SERVICE_UNAVAILABLE
    )
    ORDER_PERMISSION = (
        {'detail': 'Permission denied'},
        status.HTTP_403_FORBIDDEN
    )

    def __init__(self, msg, code=status.HTTP_400_BAD_REQUEST):
        self.msg = msg
        self.code = code
