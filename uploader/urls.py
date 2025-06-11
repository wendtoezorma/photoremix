from django.urls import path
from .views import * # importe ta vue index

urlpatterns = [
    path('', index, name='index'),
]
