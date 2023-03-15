import datetime
from django import forms
from main.models import Booking, Hotel, Client

class ManageHotelForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())

class ManageInForm(forms.Form):
    room = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super(ManageInForm, self).__init__(*args, **kwargs)
        if queryset is not None:
            self.fields['room'].queryset = queryset

class ManageOutForm(forms.Form):
    room = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super(ManageOutForm, self).__init__(*args, **kwargs)
        if queryset is not None:
            self.fields['room'].queryset = queryset
