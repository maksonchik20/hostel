
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
    path('work/<int:hotel_id>/<int:working_woman_id>/<int:room_id>/', work_apply, name="work"),
    path('work/<int:hotel_id>/<int:working_woman_id>/', work, name="work"),
    path('work/', work_select, name="work"),
]