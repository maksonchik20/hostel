
from django.urls import path
from .views import *
urlpatterns = [
    path('index/', index),
    path('some-page/', some_page)
]