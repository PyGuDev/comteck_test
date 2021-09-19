from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('guide.urls')),
    path('api/documentation/', include('terminology.doc_urls'))
]
