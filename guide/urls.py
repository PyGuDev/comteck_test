from django.urls import path

from .views import ListGuideAPIView


urlpatterns = [
    path('guide/', ListGuideAPIView.as_view(), name='list_guide'),
]
