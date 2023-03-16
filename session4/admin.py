from django.contrib import admin
from .models import *

class CostPriceAdmin(admin.ModelAdmin):
    ordering = ['-cat',]

admin.site.register(CostPrice, CostPriceAdmin)