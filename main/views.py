from django.shortcuts import render
from django.http import HttpResponse
from .models import Client, Hotel, HotelRoom
# from django_tables2 import SingleTableView
from .tables import ClientTable
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig

def index(request):
    # здесь можно получить данные из бд и передать их также в data
    table = ClientTable(Client.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"clients.{export_format}")
    data = {
        'header_text': "Клиенты",
        'text': 'Клиенты',
        'title':'Клиенты',
        'clients': Client.objects.all(),
        'table': table,
        'export_formats': ['xls', 'json', 'xlsx', 'yaml']
        }
    return render(request, 'main/index.html', data)

def root(request):
    return render(request, 'main/root.html')

def info(request):
    hotels = Hotel.objects.all()
    rooms = HotelRoom.objects.all()

    data = {
        'header_text': "Отчет",
        'hotels': hotels,
        }
    print(data['hotels'])
    return render(request, 'main/info.html', data)

