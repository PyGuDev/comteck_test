from django.core.exceptions import ValidationError
from django.db.models import Value, QuerySet
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .exceptions import BadRequestError
from .serializers import ListGuideSerializer, ListGuideItemSerializer
from .models import Guide, GuideItem, GuideVersion


class ListGuideAPIView(ListAPIView):
    """
    Вывод списка справочников

    Можно получить актуальные справочники на указанную дату
    ?date=2021-10-10 в таком формате
    """
    serializer_class = ListGuideSerializer

    def get_queryset(self):
        queryset = Guide.objects.all()
        date = self.request.query_params.get('date')
        if date:
            try:
                # Сделал фильтр актуальных на указанную дату
                queryset = Guide.objects.filter_date(date).annotate(
                    filter_date=Value(date))
            except ValidationError:
                pass
        return queryset


class ListGuideItemAPIView(ListAPIView):
    """
    Получение списка элементов спраочника

    Получаение списка элементов актуальной версии (последней)
    """
    serializer_class = ListGuideItemSerializer

    def get_queryset(self) -> QuerySet[GuideItem]:
        pk = self.kwargs.get('guide_pk')
        try:
            # Получаем актуальную версию заданного справочника
            guide = Guide.objects.get_current_version(pk)
        except Guide.DoesNotExist:
            raise Http404

        queryset = GuideItem.objects.filter(parent_id=guide)
        return queryset

    def put(self, request, **kwargs):
        """
        Проверкак входящих данных актуальной версии

        Валидация списка словарей элементов справочника"
        """
        return self._validate_items(request)

    def _validate_items(self, request):
        """Проверкак входящих данных списка словарей элементов справочника"""
        data = request.data
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        self._validate(serializer.data)
        return Response(status=status.HTTP_200_OK)

    def _validate(self, list_data: dict):
        """Проверяем наличие элементов в базе данных"""
        queryset = self.get_queryset()
        for item in list_data:
            try:
                queryset.get(**item)
            except GuideItem.DoesNotExist:
                raise BadRequestError(message=f'Item code {item.get("code_item")} invalid', code='invalid')


class ListGuideItemSelectedVersionAPIView(ListGuideItemAPIView):
    """
    Получение списка элементов выбранной версии

    Указываектся version_pk
    """

    def get_queryset(self):
        pk = self.kwargs.get('version_pk')
        try:
            guide_version = GuideVersion.objects.get(id=pk)
        except GuideVersion.DoesNotExist:
            raise Http404

        return guide_version.guide_item.all()

    def put(self, request, **kwargs):
        """
        Проверкак входящих данных заданной версии

        Валидация списка словарей элементов справочника"
        """
        return super().put(request, **kwargs)
