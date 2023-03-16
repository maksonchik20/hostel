from django.urls import path
from .views import *


urlpatterns = [
    path('', root),
    path('in/', manage_in_hotel, name="manage_in_hotel"),
    path('out/', manage_out_hotel, name="manage_out_hotel"),
    path('in/<int:id>/', manage_in_room, name="manage_in_room"),
    path('out/<int:id>/', manage_out_room, name="manage_out_room"),
]
