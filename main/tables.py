import django_tables2 as tables
from .models import Client

class ClientTable(tables.Table):
    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4-responsive.html"
        # fields = ("first_name", "last_name")

class HotelTable(tables.Table):
    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4-responsive.html"
        # fields = ("first_name", "last_name")
