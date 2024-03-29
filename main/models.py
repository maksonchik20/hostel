from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from utils.sale import calculate_price_with_sale


DIRECTION = (
    ('Популярное', 'Популярное'),
    ('Среднее по популярности', 'Среднее по популярности'),
    ('Непопулярное', 'Непопулярное')
)

class DeadSeason(models.Model):
    hotel = models.OneToOneField('Hotel', on_delete=models.CASCADE, verbose_name='Отель')
    date_start = models.DateField(verbose_name='Дата начала Мертвого сезона')
    date_end = models.DateField(verbose_name='Дата окончания мертвого сезона')

    def __str__(self):
        return f"у отеля {self.hotel.name} мертвый сезон с {self.date_start} по {self.date_end}"

    class Meta:
        verbose_name = 'Период мертвого сезона'
        verbose_name_plural = 'Периоды мертвого сезона'


class CostPrice(models.Model):
    CAT = (
        ('Стандарт', 'Стандарт'),
        ('Люкс', 'Люкс'),
        ('Апартамент', 'Апартамент')
    )
    hotel = models.ForeignKey("Hotel", on_delete=models.PROTECT, verbose_name='Отель')
    cat = models.CharField(choices=CAT, verbose_name="Категория", max_length=255)
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __str__(self):
        return f"В отеле {self.hotel.name} категория {self.cat} стоит {self.price} "

    class Meta:
        verbose_name = 'Цена номера по категории'
        verbose_name_plural = 'Цены номеров в разрезе категорий'

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
    direction = models.CharField(choices=DIRECTION, max_length=255, verbose_name="Направление", default="Среднее по популярности")

    def __str__(self):
        return f'Отель: {self.name}. Направление: {self.direction}. Местонахождение: {self.region.name}'
    
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

class Client(models.Model):
    TYPES_DOCUMENT = (
        ('Паспорт гражданина РФ', 'Паспорт гражданина РФ'),
        ('Свидетельство о рождении', 'Свидетельство о рождении')
    )
    fio = models.CharField(max_length=150, verbose_name='ФИО',blank=True, null=True)
    phone = models.CharField(null=True, blank=True, verbose_name='Телефон +7(9xx) xxx-xx-xx', max_length=255)
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
        verbose_name = 'Гости'
        verbose_name_plural = 'Гости'


class Quests(models.Model):
    PAYERS = (
        ('физ.лицо', 'физ.лицо'),
        ('юр.лицо', 'юр.лицо')
    )
    payer = models.CharField(max_length=150, verbose_name='Плательщик', null=True, blank=True)
    vid = models.CharField(max_length=255, choices=PAYERS, verbose_name='Вид')

    def __str__(self):
        return f"{self.payer}  -  {self.vid}"
    class Meta:
        verbose_name = 'Клиент (плательщик)'
        verbose_name_plural = 'Клиенты (плательщики)'

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
    users = models.TextField(verbose_name='Проживают', null=True, blank=True, editable=False)


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
    booking = models.ForeignKey("Booking", on_delete=models.PROTECT, verbose_name="Основание")
    sums = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    prepayment = models.PositiveIntegerField(verbose_name="Оплачено по факту")
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, editable=True)

    def __str__(self):
        return f"{self.booking.client.payer}. Нужная сумма:{self.sums} Оплачено: {self.prepayment}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Booking(models.Model):
    # @staticmethod
    # def check_room_is_free(value):
    #     room = HotelRoom.objects.get(pk=value.id)
    #     print(room.status)
    #     return room.status in [('Свободный (грязный)', 'Свободный (грязный)'), ('Свободный (чистый)', 'Свободный (чистый)')]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель', null=True, blank=True)
    client = models.ForeignKey(Quests, on_delete=models.PROTECT, verbose_name="плательщик", null=True, blank=True)
    date_check_in = models.DateField(verbose_name='Дата заезда')
    date_of_departure = models.DateField(verbose_name="Дата выезда")
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, verbose_name="Комната")
    nights = models.PositiveIntegerField(help_text="Вы можете заполнить поле самостоятельно или оно заполнится само после сохранения на основе данных заезда и выезда", verbose_name="Ночей", null=True, blank=True)
    pay = models.PositiveIntegerField(verbose_name="Стоимость", null=True, blank=True, help_text="Вы можете заполнить поле самостоятельно или оно заполнится автоматически после сохранения на основе данных стоимости номера. Результат вычислений можно увидеть, сохранив запись и вернувшись обратно или просто нажать 'Сохранить и продолжить редактирование'")
    cnt_people = models.PositiveIntegerField(verbose_name="Количество людей", default=1)
    result_sum = models.PositiveIntegerField(verbose_name="Итоговая цена (может выводиться со скидкой в зависимости от периода мертвого сезона отеля и его направления)", null=True, blank=True, help_text="Вы можете заполнить поле самостоятельно или оно заполнится автоматически после сохранения на основе данных стоимости номера и количестве людей. Результат вычислений можно увидеть, сохранив запись и вернувшись обратно или просто нажать 'Сохранить и продолжить редактирование'")
    flag = models.BooleanField(verbose_name="Бронь подтверждена", default=False)

    def save(self, *args, **kwargs):
        new_object = not self.pk
        if new_object: # new object
            # print('create')
            # booking = Booking.objects.get(pk=self.pk)
            # print(self.result_sum)
            # Pays.objects.create(booking=booking, sums=self.result_sum, prepayment=0)
            pay_changed = True
        super(Booking, self).save(*args, **kwargs)
        pay_changed = False
        if not new_object:
            orig_obj = Booking.objects.get(pk=self.pk)
            if orig_obj.pay != self.pay:
                pay_changed = True
        if not pay_changed:
            for price in CostPrice.objects.all():
                result_sum = price.price*self.nights
                if self.hotel.pk is price.hotel.pk:
                    hotel_date_dead = DeadSeason.objects.get(hotel=self.hotel)
                    if self.date_check_in < hotel_date_dead.date_end and self.date_check_in > hotel_date_dead.date_start:
                        a = Booking.objects.filter(pk=self.pk).update(pay=price.price, result_sum=result_sum * 0.8)
                    else:
                        a = Booking.objects.filter(pk=self.pk).update(pay=price.price, result_sum=calculate_price_with_sale(self.hotel.direction, result_sum))
        if not new_object:
            booking = Booking.objects.get(pk=self.pk)
            if len(Pays.objects.filter(booking=booking)) == 0:
                Pays.objects.create(booking=booking, sums=booking.result_sum, prepayment=0)
    def __str__(self):
        return f"{self.date_check_in} - {self.date_of_departure} | Номер: {self.hotel_room.name}"
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

class CategoryWork(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Вид работы'
        verbose_name_plural = 'Виды работ'


class Personal(models.Model):
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    work = models.ForeignKey(CategoryWork, on_delete=models.PROTECT, verbose_name="Вид работы")

    def __str__(self):
        return f"{self.fio} -- {self.work}"
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class RequestCleaning(models.Model):
    STATUS = (
        ('К выполнению', 'К выполнению'),
        ('На выполнении', 'На выполнении'),
        ('Выполнена', 'Выполнена')
    )
    date = models.DateField(verbose_name='Дата')
    cleaning_woman = models.ForeignKey(Personal, on_delete=models.CASCADE, verbose_name='ФИО Горничной')
    hotel = models.ForeignKey(Hotel, verbose_name="Отель", on_delete=models.CASCADE)
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, verbose_name='Номер к уборке')
    status = models.CharField(choices=STATUS, verbose_name="Статус", max_length=255)
    def __str__(self):
        return f"{self.date} -- {self.cleaning_woman}. {self.hotel.name} - Номер: {self.room.name}. Статус: {self.status}"
    
    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
# signals

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=Booking)
def update_stock(sender, instance, **kwargs):
    # print(kwargs)
    instance.nights = (instance.date_of_departure - instance.date_check_in).days
    booking = Booking.objects.get(pk=instance.pk)
    post_save.disconnect(update_stock, sender=Booking)
    instance.save()
    post_save.connect(update_stock, sender=Booking)
    # if kwargs['created']:
    #     print(instance.result_sum)
        # Pays.objects.create(booking=booking, sums=instance.result_sum, prepayment=0)


@receiver(post_save, sender=Pays)
def update_pays(sender, instance, **kwargs):
    if instance.prepayment >= instance.sums:
        booking = instance.booking
        booking = Booking.objects.filter(pk=booking.pk).update(flag=True)
    post_save.disconnect(update_pays, sender=Pays)
    instance.save()
    post_save.connect(update_pays, sender=Pays)

