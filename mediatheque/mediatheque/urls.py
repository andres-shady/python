
from django.contrib import admin
from django.urls import path, include
from . import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bibliothecaire/', include('bibliothecaire.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.list_media_view, name='list_media_membre'),
]
