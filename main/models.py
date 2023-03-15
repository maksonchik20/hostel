from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField



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
    TYPES_DOCUMENT = (
        ('Паспорт гражданина РФ', 'Паспорт гражданина РФ'),
        ('Свидетельство о рождении', 'Свидетельство о рождении')
    )
    fio = models.CharField(max_length=150, verbose_name='ФИО',blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True, verbose_name='Телефон +7(9xx) xxx-xx-xx')
    date_birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    email = models.EmailField(verbose_name='Почта', blank=True)
    type_doc = models.CharField(choices=TYPES_DOCUMENT, max_length=255, verbose_name='Тип документа')
    series_doc = models.PositiveIntegerField(verbose_name='Серия')
    num_doc = models.CharField(verbose_name='Номер', max_length=255)
    code_podr_doc = models.PositiveIntegerField(verbose_name='Код подразделения')
    issued_by_doc = models.CharField(max_length=255, verbose_name="Кем выдан")

    def __str__(self):
        return f'{self.fio}'
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Quests(models.Model):
    PAYERS = (
        ('физ.лицо', 'физ.лицо'),
        ('юр.лицо', 'юр.лицо')
    )

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
    count_place = models.PositiveIntegerField(verbose_name='Количество мест', blank=True, null=True)
    cat = models.CharField(choices=CAT, verbose_name="Категория", max_length=255)
    status = models.CharField(choices=STATUS, max_length=255, verbose_name="Статус")


    def __str__(self):
        return f"Номер: {self.name} Категория: {self.cat} Статус: {self.status}"

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
    

class RoomOccupancy(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, verbose_name='Номер', validators=[])
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

class Pays(models.Model):
    booking = models.ForeignKey("Booking", on_delete=models.PROTECT)
    sums = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    prepayment = models.PositiveIntegerField(verbose_name="Предоплата")

class Booking(models.Model):
    @staticmethod
    def check_room_is_free(value):
        room = HotelRoom.objects.get(pk=value.id)
        print(room.status)
        return room.status in [('Свободный (грязный)', 'Свободный (грязный)'), ('Свободный (чистый)', 'Свободный (чистый)')]

    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, verbose_name='Отель', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Клиент")
    date_check_in = models.DateField(verbose_name='Дата заезда')
    date_of_departure = models.DateField(verbose_name="Дата выезда")
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, verbose_name="Комната")
    nights = models.PositiveIntegerField(help_text="Вы можете заполнить поле самостоятельно или оно заполнится само после сохранения на основе данных заезда и выезда", verbose_name="Ночей", null=True, blank=True)
    pay = models.PositiveIntegerField(verbose_name="Стоимость", null=True, blank=True)
    flag = models.BooleanField(verbose_name="Бронь подтверждена", default=False)

    def clean(self):
        self.is_cleaned = True
        if not self.check_room_is_free(self.hotel_room):
            raise ValidationError("Комната не свободна!")
        super(RoomOccupancy, self).clean()

    def __str__(self):
        return f"{self.date_check_in} - {self.date_of_departure} | Номер: {self.hotel_room.name}"
    # def save(self, *args, **kwargs):
    #     print(args, kwargs)
    #     super(Booking, self).save(*args, **kwargs)  
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


# signals

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta

@receiver(post_save, sender=Booking)
def update_stock(sender, instance, **kwargs):
    instance.nights = (instance.date_of_departure - instance.date_check_in).days
    booking = Booking.objects.get(pk=instance.pk)
    print(booking)
    if kwargs['created']:
        Pays.objects.create(booking=booking, sums=instance.pay, prepayment=0)
    post_save.disconnect(update_stock, sender=Booking)
    instance.save()
    post_save.connect(update_stock, sender=Booking)


# @receiver(pre_save, sender=Booking)
# def for_book(sender, instance, **kwargs):
#     print(instance, kwargs)
#     post_save.disconnect(for_book, sender=Booking)
#     instance.save()
#     post_save.connect(for_book, sender=Booking)


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



