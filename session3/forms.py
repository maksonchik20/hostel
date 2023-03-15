import datetime
from django import forms
from main.models import Booking, Hotel

class ManageInHotelForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())

class ManageInForm(forms.Form):

    room = forms.ModelChoiceField(queryset=Booking.objects.filter(date_check_in=datetime.datetime.now()))