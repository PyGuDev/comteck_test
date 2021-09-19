from rest_framework.generics import ListAPIView
from .serializers import ListGuideSerializer
from .models import Guide


class ListGuideAPIView(ListAPIView):
    serializer_class = ListGuideSerializer
    queryset = Guide.objects.all()
