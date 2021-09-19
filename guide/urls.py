from django.urls import path

from .views import ListGuideAPIView, ListGuideItemAPIView


urlpatterns = [
    path('guide/', ListGuideAPIView.as_view(), name='list_guide'),
    path('guide/<slug:pk>/items/current/', ListGuideItemAPIView.as_view(), name='list_guide_item')
]
