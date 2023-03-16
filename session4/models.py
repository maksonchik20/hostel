from django.db import models
from main.models import *


class CostPrice(models.Model):
    CAT = (
        ('Стандарт', 'Стандарт'),
        ('Люкс', 'Люкс'),
        ('Апартамент', 'Апартамент')
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, verbose_name='Отель')
    cat = models.CharField(choices=CAT, verbose_name="Категория", max_length=255)
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __str__(self):
        return f"В отеле {self.hotel.name} категория {self.cat} стоит {self.price} "

    class Meta:
        verbose_name = 'Цена номера по категории'
        verbose_name_plural = 'Цены номеров в разрезе категорий'
    