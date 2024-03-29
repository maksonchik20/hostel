from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Client, Hotel, HotelRoom, Booking, Pays, Region,CostPrice, RequestCleaning, Personal, CategoryWork
from .models import Client, Hotel, Personal, RequestCleaning, HotelRoom, Booking, Pays, Region,CostPrice
from django.views.generic import ListView
from .tables import ClientTable
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
import random
import json
from datetime import date, datetime, timedelta
from dataclasses import dataclass
from typing import List
from .forms import ReportSelectForm, WorkSelectForm, WorkApplyForm
# from session4.models import CostPrice
from django.db.models import Q



def create_data():
    ...
    prices = [2500, 3800, 4000, 4500, 5000]
    CAT = (
        ('Стандарт', 'Стандарт'),
        ('Люкс', 'Люкс'),
        ('Апартамент', 'Апартамент')
    )
    for hotel in Hotel.objects.all():
        for cat in CAT:
            CostPrice.objects.create(hotel=hotel, cat=cat[0], price=random.choice(prices))
    # regs = set()
    # with open('russia', 'r', encoding='utf-8') as f:
    #     r = json.loads(f.read())
    #     for el in r:
    #         if el['region'] not in regs:
    #             regs.add(el['region'])
    #             Region.objects.create(name=el['region'])
    # STATUS = (
    #     ('Занят', 'Занят'),
    #     ('Занят (грязный)', 'Занят (грязный)'),
    #     ('Свободный (грязный)', 'Свободный (грязный)'),
    #     ('Свободный (чистый)', 'Свободный (чистый)')
    # )
    # for hotel in Hotel.objects.all():
    #     for i in range(1, 7):
    #         HotelRoom.objects.create(hotel=hotel, name=i, count_place=2, cat=CAT[0][0], status=random.choice(STATUS)[0])
    # for hotel in Hotel.objects.all():
    #     for i in range(7, 10):
    #         HotelRoom.objects.create(hotel=hotel, name=i, count_place=2, cat=CAT[1][0], status=random.choice(STATUS[0]))
    # for hotel in Hotel.objects.all():
    #     for i in range(10, 12):
    #         HotelRoom.objects.create(hotel=hotel, name=i, count_place=2, cat=CAT[2][0], status=random.choice(STATUS[0]))
    
    
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
    # create_data()
    # print('good create')
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

def report(request, hotel_id, day, month, year):
    date = datetime(year=year, month=month, day=day)
    hotel = Hotel.objects.get(pk=hotel_id)
    bookings = Booking.objects.filter(hotel=hotel, date_check_in__lte=date, date_of_departure__gte=date, flag=True) # date_check_in__range=(date(2023,3,22), date(2023,3,24))
    nights = 0
    sell_sum = 0
    total_rooms = len(HotelRoom.objects.filter(hotel=hotel))
    for el in bookings:
        nights += 1
        sell_sum += el.pay
    if nights == 0:
        return render(request, "main/reports.html", {'header_text': "Аналитика",
                                                  'report': {
                                                    'show': True,
                                                    'date': date,
                                                    'hotel_name': hotel.name,
                                                    'nights': 0,
                                                    'sell_sum': 0,
                                                    'load': 0,
                                                    'adr': 0,
                                                    'revpar': 0
                                                  }})
    
    load = int(nights / total_rooms * 10000) / 100
    adr = sell_sum / nights
    revpar = sell_sum / total_rooms

    return render(request, "main/reports.html", {'header_text': "Аналитика",
                                                  'report': {
                                                    'show': True,
                                                    'date': date,
                                                    'hotel_name': hotel.name,
                                                    'nights': nights,
                                                    'sell_sum': sell_sum,
                                                    'load': load,
                                                    'adr': adr,
                                                    'revpar': revpar
                                                  }})

def report_select(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReportSelectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            date = form.cleaned_data["date"].strftime(r'%d/%m/%Y')
            return HttpResponseRedirect(f'/report/{form.cleaned_data["hotel"].id}/{date}')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReportSelectForm()

    return render(request, "main/reports_select.html", {'form': form, 'header_text': "Аналитика",})


def work_select(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WorkSelectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(f'/work/{form.cleaned_data["hotel"].id}/{form.cleaned_data["cleaning_woman"].id}')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = WorkSelectForm()

    return render(request, "main/work_select.html", {'form': form, 'header_text': "Формирование заявок на работу",})


def report_sell_nights(request):
    data = {'hotels': [],  'header_text': "Аналитика",}
    date_now = datetime.now()
    for hotel in Hotel.objects.all():
        data['hotels'].append({'hotel': hotel.name, 'info': [], 'result_sum': 0, 'hotel_id': hotel.pk}) 
        for i in range(-5, 31):
            a = Booking.objects.filter(hotel=hotel, date_check_in__lte=date_now + timedelta(days=i), date_of_departure__gte=date_now + timedelta(days=i), flag=True) # date_check_in__range=(date(2023,3,22), date(2023,3,24))
            data['hotels'][-1]['info'].append({'date': date_now + timedelta(days=i), 'sums': 0, 'nights': 0})
            for el in a:
                data['hotels'][-1]['info'][-1]['sums'] += el.pay
                data['hotels'][-1]['info'][-1]['nights'] += 1
                print(el.nights)
                data['hotels'][-1]['result_sum'] += el.pay
                
    return render(request, 'main/sell_nights.html', data)


def analysis_cleaning(request):
    data = {'cleaning_data': {}, 'fio': []}
    for fio_cleaning in Personal.objects.filter(work=CategoryWork.objects.get(name='Горничная')):
        data['cleaning_data'][f'{fio_cleaning.fio}'] = {'to_cleaning': 0, 'completed': 0, 'progress': 0}
        data['fio'].append(fio_cleaning.fio)
    for el in RequestCleaning.objects.all():
        for fio in data['fio']:
            if el.cleaning_woman.fio == fio:
                if el.status == 'К выполнению':
                    data['cleaning_data'][f'{el.cleaning_woman.fio}']['to_cleaning'] += 1
                elif el.status == 'На выполнении':
                    data['cleaning_data'][f'{el.cleaning_woman.fio}']['progress'] += 1
                elif el.status == 'Выполнена':
                    data['cleaning_data'][f'{el.cleaning_woman.fio}']['completed'] += 1
    data['cleaning_data'] = data['cleaning_data'].items()
    return render(request, 'main/analysis_cleaning.html', data)
def work(request, hotel_id, working_woman_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    
    forms = [
        {"form": WorkApplyForm(), "room": room.id} 
        for 
        room 
        in 
        HotelRoom.objects.filter(hotel=hotel).filter(Q(status="Занят (грязный)") | Q(status="Свободный (грязный)")).order_by("name")
        if 
        len(RequestCleaning.objects.filter(room=room, hotel=hotel)) == 0
    ]
    return render(request, "main/work.html", {'header_text': "Аналитика",
                                                  'forms': forms, 'hotel_id': hotel_id, "working_woman_id": working_woman_id})

def work_apply(request, hotel_id, working_woman_id, room_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    room = HotelRoom.objects.get(pk=room_id, hotel=hotel)
    working_woman = Personal.objects.get(pk=working_woman_id)

    if request.method == 'POST':

        RequestCleaning.objects.create(
            date=datetime.now(),
            cleaning_woman=working_woman,
            hotel=hotel,
            room=room,
            status="К выполнению"
        )

        return HttpResponseRedirect(f'/work/{hotel_id}/{working_woman_id}')
    
