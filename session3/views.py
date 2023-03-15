from django.shortcuts import render
from .forms import ManageInForm, ManageInHotelForm
from .models import CheckIn
from django.http import HttpResponseRedirect
import datetime

def root(request):
    return render(request, "session3/managing.html")

def manage_in_room(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ManageInForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            clients = form.cleaned_data["people"]
            room = form.cleaned_data["room"]

            print(clients, room)

            CheckIn.objects.create(
                date_in=datetime.datetime.now(),
                room = room,
                peoples=[clients]
            )
            
            return HttpResponseRedirect('/managing')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ManageInForm()

    return render(request, 'session3/in_room.html', {'form': form, 'header_text': "Оформление заезда"})


def manage_in(request, id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ManageInForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/managing')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ManageInForm()

    return render(request, 'session3/in.html', {'form': form, 'header_text': "Оформление заезда", 'id': id})

def manage_in_hotel(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ManageInHotelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.cleaned_data["hotel"].id)
            return HttpResponseRedirect(f'/managing/in/{form.cleaned_data["hotel"].id}')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ManageInHotelForm()

    return render(request, 'session3/in_hotel.html', {'form': form, 'header_text': "Оформление заезда",})