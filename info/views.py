from django.shortcuts import render
from ..main.models import Hotel

def root(request):
    return render(request, 'info/root.html', {'hotels': []})

def hotel(request):
    return render(request, 'info/hotel.html')

def info(request):
    table = Hotel.objects.all()
    data = {
        'header_text': "Отчет",
        'hotels': table
        }
    return render(request, 'info/info.html', data)

