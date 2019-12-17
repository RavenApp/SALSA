from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('setup/', create),
    path('how-to/', howto),
    path('dashboard/', find_dash),
    path('dashboard/<int:pk>/', dashboard),
]
