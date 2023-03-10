from django.db import models
from django.contrib.auth.models import AbstractUser




# class User(AbstractUser):
#     phone = models.CharField(max_length=255, null=True, blank=True)
#     date_birthday = models.DateField(null=True, blank=True)

    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'
    
    # class Meta:
    #     verbose_name = 'Пользователь'
    #     verbose_name_plural = 'Пользователи'

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




class CategoryRoom(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория номера'
        verbose_name_plural = 'Категории номеров'

class HotelRoom(models.Model):
    STATUS = (
        ('Занят', 'Занят'),
        ('Свободный грязный', 'Свободный грязный'),
        ('Свободный чистый', 'Свободный чистый')
    )

    name = models.CharField(max_length=255, verbose_name="Название")
    cat = models.ForeignKey(CategoryRoom, on_delete=models.PROTECT, verbose_name="Категория")
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Цена")
    status = models.CharField(choices=STATUS, max_length=255, verbose_name="Статус")

    def __str__(self):
        return f"Номер: {self.name} Категория: {self.cat.name} Статус: {self.status}"

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
    







