from django import forms
from .models import Hotel

class ReportSelectForm(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'

    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())
    date = forms.DateField(widget=DateInput)
