from django.shortcuts import render
from django.http import HttpResponse
from .models import Client, Hotel, HotelRoom, Booking
from django.views.generic import ListView
from .tables import ClientTable
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
import random


def create_data():
    STATUS = (
        ('Занят', 'Занят'),
        ('Занят (грязный)', 'Занят (грязный)'),
        ('Свободный (грязный)', 'Свободный (грязный)'),
        ('Свободный (чистый)', 'Свободный (чистый)')
    )
    CAT = (
        ('Стандарт', 'Стандарт'),
        ('Люкс', 'Люкс'),
        ('Апартамент', 'Апартамент')
    )
    for hotel in Hotel.objects.all():
        for i in range(1, 7):
            HotelRoom.objects.create(hotel=hotel, name=i, count_place=2, cat=CAT[0][0], status=random.choice(STATUS))
    for hotel in Hotel.objects.all():
        for i in range(7, 10):
            HotelRoom.objects.create(hotel=hotel, name=i, count_place=2, cat=CAT[1][0], status=random.choice(STATUS))
    for hotel in Hotel.objects.all():
        for i in range(10, 12):
            HotelRoom.objects.create(hotel=hotel, name=i, count_place=2, cat=CAT[2][0], status=random.choice(STATUS))
    
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
    create_data()
    print('good create')
    # Booking.objects.all().delete()
    return render(request, 'main/index.html', data)

def root(request):
    return render(request, 'main/root.html')

def info(request):
    rooms = HotelRoom.objects.all()

    data = {
        'header_text': "Отчет",
        'rooms': rooms,
        }

    return render(request, 'main/info.html', data)

def bron(request):
    occ = Booking.objects.all()

    data = {
        'header_text': "Журнал бронирования",
        'occ': occ,
        }

    return render(request, 'main/bron.html', data)


class BookingListView(ListView):
    model = Booking
    template_name = "django_tables2/bootstrap.html"
