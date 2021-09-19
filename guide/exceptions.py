from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, code: str):
        detail = {'message': message, 'code': code}
        super().__init__(detail=detail)
