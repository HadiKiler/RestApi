from django.contrib import admin
from django.urls import path, include

from .views import api_home

urlpatterns = [
    path('', api_home),
    path('person/', include('person.urls')),
    path('person2/', include('person.router')),
]
