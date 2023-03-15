from django.urls import path
from .views import *


urlpatterns = [
    path('', root),
    # path('in/<int:id>/', manage_in, name="manage_in"),
    path('in/', manage_in_room, name="manage_in_room"),
    path('out/', manage_out_room, name="manage_out_room"),
]
