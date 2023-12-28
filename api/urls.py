from django.contrib import admin
from django.urls import path, include
from person.views import show
from .views import api_home

urlpatterns = [
    path('', show),
    path('person/', include('person.urls')),
    path('person2/', include('person.router')),
]
