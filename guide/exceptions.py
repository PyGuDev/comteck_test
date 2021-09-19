from typing import Optional

from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, code: str, data: Optional[dict] = None):
        detail = {'message': message, 'code': code}
        if data:
            detail.update(data)
        super().__init__(detail=detail)
