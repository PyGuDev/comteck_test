from drf_yasg import openapi
from rest_framework import serializers


class ErrorResponseSchema(serializers.Serializer):
    message = serializers.CharField()
    code = serializers.CharField()

class ErrorDataResponseSchema(ErrorResponseSchema):
    code_item = serializers.ListSerializer(child=serializers.CharField())


class ValidateGuideItemSchema:
    responses: dict = {
        "400": openapi.Response(
            description="Невалидные элементы",
            schema=ErrorDataResponseSchema,
            examples={
                "application/json": {
                    "message": "Items invalid",
                    "code": "invalid",
                    "code_ite": ['FFS', 'DASD']
                }
            }
        ),
        "400": openapi.Response(
            description="Невалидный элемент",
            schema=ErrorResponseSchema,
            examples={
                "application/json": {
                    "message": "Item code FFF invalid",
                    "code": "invalid"
                }
            }
        )
    }