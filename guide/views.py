from django.core.exceptions import ValidationError
from django.db.models import Value
from django.http import Http404
from rest_framework.generics import ListAPIView
from .serializers import ListGuideSerializer, ListGuideItemSerializer
from .models import Guide, GuideItem


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
    Получение элементов спраочника

    Получаение элементы актуальной версии (последней)
    """
    serializer_class = ListGuideItemSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        try:
            guide = Guide.objects.get_current_version(pk)
        except Guide.DoesNotExist:
            raise Http404
        queryset = GuideItem.objects.filter(parent_id=guide)
        return queryset
