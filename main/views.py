from django.shortcuts import render
from django.http import HttpResponse
from .models import Client


def index(request):
    # здесь можно получить данные из бд и передать их также в data
    data = {
        'text': 'some text from python views.py',
        'title':'Клиенты',
        'clients': Client.objects.all()
        }
    return render(request, 'main/index.html', data)

def some_page(request):
    return HttpResponse('hello')
