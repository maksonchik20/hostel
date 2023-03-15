import datetime
from django import forms
from main.models import Booking, Hotel, Client

class ManageHotelForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())

class ManageInForm(forms.Form):
    people = forms.ModelChoiceField(queryset=Client.objects.all())
    room = forms.ModelChoiceField(queryset=Booking.objects.filter(date_check_in=datetime.datetime.now()))

class ManageOutForm(forms.Form):
    room = forms.ChoiceField(choices=())

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        print(choices)
        super(ManageOutForm, self).__init__(*args, **kwargs)
        if choices is not None:
            self.fields['room'].choices = choices
