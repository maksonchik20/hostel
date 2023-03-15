from django.db import models
from main.models import *


class CheckIn(models.Model):
    date_in = models.DateField(verbose_name="Дата заезда")
    brone = models.ForeignKey(Booking, on_delete=models.PROTECT, verbose_name="Бронирование")
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, verbose_name="Отель")
    room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, verbose_name="Номер")
    date_out = models.DateField(verbose_name="Дата выезда")
    peoples = models.ManyToManyField(Client, verbose_name="Список прибывших гостей")

    def __str__(self):
        return f"{self.hotel.name} Номер: {self.room.name}. {self.date_in} по {self.date_out}"

    class Meta:
        verbose_name = 'Заезд'
        verbose_name_plural = 'Заезды'

class CheckOut(models.Model):
    date_out = models.DateField(verbose_name="Дата выезда")
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, verbose_name="Отель")
    room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT, verbose_name="Освобождаемый номер")
    peoples = models.ManyToManyField(Client, verbose_name="Список убывших гостей")
    brone = models.ForeignKey(Booking, on_delete=models.PROTECT, verbose_name="Бронирование", null=True, blank=True)
    def __str__(self):
        return f"{self.hotel.name} Номер: {self.room.name}. Дата: {self.date_out}"

    class Meta:
        verbose_name = 'Выезд'
        verbose_name_plural = 'Выезды'
# signals

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=CheckOut)
def update_check_out(sender, instance, **kwargs):
    users = ""
    room = HotelRoom.objects.filter(pk=instance.room.pk)
    users_in = room[0].users.split('\n')
    result_users_in = users_in.copy()
    for people in instance.peoples.all():
        for user_in in users_in:
            if people.fio in user_in:
                result_users_in.remove(user_in)
    users_in = "\n".join(result_users_in)
    room.update(status="Свободный (грязный)", users=users_in)
    post_save.disconnect(update_check_out, sender=CheckOut)
    instance.save()
    post_save.connect(update_check_out, sender=CheckOut)

@receiver(post_save, sender=CheckIn)
def update_check_in(sender, instance, **kwargs):
    users = ""
    for people in instance.peoples.all():
        users += people.fio + f" с {instance.date_in} по {instance.date_out}" + '\n'
    room = HotelRoom.objects.filter(pk=instance.room.pk)
    room.update(status="Занят", users=room[0].users + users)
    post_save.disconnect(update_check_in, sender=CheckIn)
    instance.save()
    post_save.connect(update_check_in, sender=CheckIn)

