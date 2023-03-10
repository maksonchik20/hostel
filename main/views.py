from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('test')

def some_page(request):
    return HttpResponse('hello')
