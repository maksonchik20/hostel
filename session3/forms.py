import datetime
from django import forms
from main.models import Booking, Hotel, Client

class ManageInHotelForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())

class ManageInForm(forms.Form):
    people = forms.ModelChoiceField(queryset=Client.objects.all())
    room = forms.ModelChoiceField(queryset=Booking.objects.filter(date_check_in=datetime.datetime.now()))