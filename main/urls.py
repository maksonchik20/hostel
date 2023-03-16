
from django.urls import path, include
from .views import *

urlpatterns = [
    path('index/', index),
    # path('info/', include("info.urls")),
    path('', root),
    path('info/', info),
    path('bron/', bron),
    path('sell-nights/', report_sell_nights),
    path('report/<int:hotel_id>/<int:day>/<int:month>/<int:year>/', report, name="report"),
    path('report/', report_select, name="report"),
]