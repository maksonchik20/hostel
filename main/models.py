from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError




# class User(AbstractUser):
#     phone = models.CharField(max_length=255, null=True, blank=True)
#     date_birthday = models.DateField(null=True, blank=True)

    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'
    
    # class Meta:
    #     verbose_name = 'Пользователь'
    #     verbose_name_plural = 'Пользователи'

class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'Название: {self.name}'
    
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

class Hotel(models.Model):
    name = models.CharField(max_length=150)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return f'Отель: {self.name}. Местонахождение: {self.region.name}'
    
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

class Client(models.Model):
    SEX = (
        ('м', 'м'),
        ('ж', 'ж')
    )
    TYPES_DOCUMENT = (
        ('Паспорт гражданина РФ', 'Паспорт гражданина РФ'),
        ('Свидетельство о рождении', 'Свидетельство о рождении')
    )
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    surname = models.CharField(max_length=255, verbose_name='Отчество')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Телефон')
    date_birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    sex = models.CharField(choices=SEX, max_length=255, verbose_name='Пол')
    email = models.EmailField(verbose_name='Почта', blank=True)
    type_doc = models.CharField(choices=TYPES_DOCUMENT, max_length=255, verbose_name='Тип документа')
    series_doc = models.PositiveIntegerField(verbose_name='Серия')
    num_doc = models.CharField(verbose_name='Номер', max_length=255)
    code_podr_doc = models.PositiveIntegerField(verbose_name='Код подразделения')
    issued_by_doc = models.CharField(max_length=255, verbose_name="Кем выдан")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'




# class CategoryRoom(models.Model):
#     name = models.CharField(max_length=150, verbose_name='Название')
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name = 'Категория номера'
#         verbose_name_plural = 'Категории номеров'

class HotelRoom(models.Model):
    STATUS = (
        ('Занят', 'Занят'),
        ('Занят (грязный)', 'Занят (грязный)'),
        ('Свободный (грязный)', 'Свободный (грязный)'),
        ('Свободный (чистый)', 'Свободный (чистый)')
    )
    CAT = (
        ('Стандарт', 'Стандарт'),
        ('Люкс', 'Люкс'),
        ('Апартамент', 'Апартамент')
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, verbose_name='Отель')
    name = models.CharField(max_length=10, verbose_name="Номер")
    cat = models.CharField(choices=CAT, verbose_name="Категория", max_length=255)
    status = models.CharField(choices=STATUS, max_length=255, verbose_name="Статус")


    def __str__(self):
        return f"Номер: {self.name} Категория: {self.cat} Статус: {self.status}"

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
    

class RoomOccupancy(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, verbose_name='Номер')
    date_check_in = models.DateField(verbose_name="Дата заезда")
    date_of_departure = models.DateField(verbose_name='Даты выезда')

    def __str__(self):
        return f"Номер: {self.room.name} Даты: {self.date_check_in} - {self.date_of_departure}"

    class Meta:
        verbose_name = 'Занятость номера'
        verbose_name_plural = 'Занятости номеров'
    
    def clean(self):
        self.is_cleaned = True
        if self.date_check_in > self.date_of_departure:
            raise ValidationError("Дата заезда позже даты выезда!")
        super(RoomOccupancy, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(RoomOccupancy, self).save(*args, **kwargs)

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент")
    date_check_in = models.DateField(verbose_name='Дата заезда')
    time_check_in = models.TimeField(verbose_name="Время заезда")
    date_of_departure = models.DateField(verbose_name="Дата выезда")
    time_of_departure = models.TimeField(verbose_name="Время выезда")
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, verbose_name="Отель")
    big_people = models.PositiveIntegerField(verbose_name="Взрослых")
    small_people = models.PositiveIntegerField(verbose_name="Детей")
    nights = models.PositiveIntegerField(help_text="Вы можете заполнить поле самостоятельно или оно заполнится само после сохранения на основе данных заезда и выезда", verbose_name="Ночей", null=True, blank=True)


    def __str__(self):
        return f"{self.date_check_in} - {self.date_of_departure} | Номер: {self.hotel_room.name}"
    


# signals

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

@receiver(post_save, sender=Booking)
def update_stock(sender, instance, **kwargs):
    instance.nights = (instance.date_of_departure - instance.date_check_in).days
    post_save.disconnect(update_stock, sender=Booking)
    instance.save()
    post_save.connect(update_stock, sender=Booking)


# @receiver(post_save, sender=RoomOccupancy)
# def update_stock(sender, instance, **kwargs):
#     if instance.date_check_in < instance.date_of_departure:
#         print('good')
#     else:
#         print('error')
#         raise ValidationError('Дата заезда позже даты выезда')
#     post_save.disconnect(update_stock, sender=RoomOccupancy)
#     instance.save()
#     post_save.connect(update_stock, sender=RoomOccupancy)



