from django.shortcuts import render
from main.models import CostPrice

# Create your views here.

def view(request):
    prices_standard = CostPrice.objects.filter(cat="Стандарт").order_by("hotel")
    prices_luks = CostPrice.objects.filter(cat="Люкс").order_by("hotel")
    prices_app = CostPrice.objects.filter(cat="Апартамент").order_by("hotel")

    return render(request, 'session4/view.html', {
        'header_text': "Прайс-лист",
        "prices_standard": prices_standard,
        "prices_luks": prices_luks,
        "prices_app": prices_app
    })
