
from django.urls import path, include
from .views import *

urlpatterns = [
    path('index/', index),
    # path('info/', include("info.urls")),
    path('', root),
    path('info/', info),
    path('bron/', bron),
    path('report/', report),
    path('sell-nights/', report_sell_nights)
]