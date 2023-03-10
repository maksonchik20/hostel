
from django.urls import path
from .views import *
urlpatterns = [
    path('', index),
    path('some-page/', some_page)
]