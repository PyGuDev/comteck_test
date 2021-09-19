from django.core.exceptions import ValidationError
from django.db.models import Value
from rest_framework.generics import ListAPIView
from .serializers import ListGuideSerializer
from .models import Guide


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
                # Сделал филтр актуальных на указанную дату
                queryset = queryset.annotate(
                    filter_date=Value(date)).filter(
                    guide_version__date_created__gte=date).distinct('name')
            except ValidationError:
                pass
        return queryset
