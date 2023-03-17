from django.shortcuts import render
from .forms import ManageInForm, ManageHotelForm, ManageOutForm
from .models import CheckIn, CheckOut
from django.http import HttpResponseRedirect
from main.models import Booking, Hotel
import datetime

def root(request):
    return render(request, "session3/managing.html")

def manage_in_room(request, id):
    queryset = Booking.objects.filter(date_check_in=datetime.datetime.now(), hotel=id)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ManageInForm(request.POST, queryset=queryset)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            brone = form.cleaned_data["room"]
            hotel = Hotel.objects.get(pk=id)

            CheckIn.objects.create(
                date_in=datetime.datetime.now(),
                brone=brone,
                hotel=hotel,
                room=brone.hotel_room,
                date_out=brone.date_of_departure,
            ).peoples.set([brone.client.id])
            
            return HttpResponseRedirect('/managing')
 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ManageInForm(queryset=queryset)

    return render(request, 'session3/in_room.html', {'form': form, 'header_text': "Оформление заезда", "id": id})

def manage_out_room(request, id):
    queryset = Booking.objects.filter(date_of_departure=datetime.datetime.now(), hotel=id)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ManageOutForm(request.POST, queryset=queryset)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            brone = form.cleaned_data["room"]
            hotel = Hotel.objects.get(pk=id)

            CheckOut.objects.create(
                date_out=datetime.datetime.now(),
                brone=brone,
                hotel=hotel,
                room=brone.hotel_room
            ).peoples.set([brone.client.id])
            
            return HttpResponseRedirect('/managing')
 
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ManageOutForm(queryset=queryset)

    return render(request, 'session3/out_room.html', {'form': form, 'header_text': "Оформление выезда", "id": id})


def manage_out_hotel(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ManageHotelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.cleaned_data["hotel"].id)
            return HttpResponseRedirect(f'/managing/out/{form.cleaned_data["hotel"].id}')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ManageHotelForm()

    return render(request, 'session3/out_hotel.html', {'form': form, 'header_text': "Оформление выезда",})
def manage_in_hotel(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ManageHotelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(f'/managing/in/{form.cleaned_data["hotel"].id}')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ManageHotelForm()

    return render(request, 'session3/in_hotel.html', {'form': form, 'header_text': "Оформление заезда",})