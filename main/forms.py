from django import forms
from .models import CategoryWork, Hotel, Personal

class ReportSelectForm(forms.Form):
    class DateInput(forms.DateInput):
        input_type = 'date'

    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())
    date = forms.DateField(widget=DateInput)

class WorkSelectForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all())
    cleaning_woman = forms.ModelChoiceField(queryset=Personal.objects.filter(work=CategoryWork.objects.get(name="Горничная")))


class WorkApplyForm(forms.Form):
    pass

