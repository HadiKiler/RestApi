from django.contrib import admin
from django.urls import path
from .views import *

# urlpatterns = [
#     path('', PersonMixinView.as_view()),
#     path('<int:pk>', PersonMixinView.as_view()), <--- this has problem
# ]

# urlpatterns = [
#     path('', PersonListCreateView.as_view()),
#     path('<int:pk>', PersonDetailsView.as_view()),
#     path('<int:pk>/update/', ProductUpdateAPIView.as_view()),
#     path('<int:pk>/delete/', ProductDestroyAPIView.as_view()),
# ]

from .viewset import *

urlpatterns = [
    path('search/', PersonSearch.as_view()),
    path('', PersonViewSet.as_view({'get': "list", "post": "create"})),
    path('<int:pk>/', PersonViewSet.as_view({'get': 'retrieve', "put": "update", 'delete': 'destroy'}))
]
