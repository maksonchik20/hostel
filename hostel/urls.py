from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.index_title = "Администрирование Turbis-Dev"
admin.site.site_title = "Администрирование Turbis-Dev"
admin.site.site_header = "Администрирование Turbis-Dev"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('managing/', include('session3.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('prices/', include('session4.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)