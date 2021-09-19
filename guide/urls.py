from django.urls import path

from .views import ListGuideAPIView, ListGuideItemAPIView, ListGuideItemSelectedVersionAPIView


urlpatterns = [
    path('guide/', ListGuideAPIView.as_view(), name='list_guide'),
    path('guide/<slug:guide_pk>/items/current', ListGuideItemAPIView.as_view(), name='list_guide_item_current'),
    path('guide/version/<slug:version_pk>/items', ListGuideItemSelectedVersionAPIView.as_view(),
         name='list_guide_item_selected_version')
]
