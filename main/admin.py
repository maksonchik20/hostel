from django.contrib import admin
from .models import HotelRoom, Client, Booking, RoomOccupancy, Hotel, Region, Pays, Quests
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class CustomClient(admin.ModelAdmin):
    model = Client
    list_display = ['fio', 'phone', 'email']
    list_filter = ['date_birthday']
    search_fields = ['fio', 'num_doc', 'phone', 'email']
    fieldsets = (
        ( 
            None, 
            {
                'fields': 
                (
                    'fio', 
                    'date_birthday'
                )
            }
        ),
        (
            'Контактная информация',
            {
                'fields': (
                    'phone',
                    'email'
                )
            }
        ),
        (
            'Паспортные данные',
            {
                'fields': (
                    'type_doc',
                    'series_doc',
                    'num_doc',
                    'code_podr_doc',
                    'issued_by_doc'
                )
            }
        )
    )


class BookingAdmin(admin.ModelAdmin):
    # readonly_fields = ('nights', )
    pass
class HotelRoomAdmin(admin.ModelAdmin):
    readonly_fields = ('users', )
    

admin.site.register(Client, CustomClient)
admin.site.register(HotelRoom, HotelRoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(RoomOccupancy)
admin.site.register(Hotel)
admin.site.register(Region)
admin.site.register(Pays)
admin.site.register(Quests)




# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import User

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = User
#     list_display = ['first_name', 'last_name', 'phone', 'date_birthday']
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Other Personal info',
#             {
#                 'fields': (
#                     'phone', 
#                     'date_birthday'
#                 )
#             }
#         )
#     )
#     add_fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Other Personal info',
#             {
#                 'fields': (
#                     'phone', 
#                     'date_birthday'
#                 )
#             }
#         )
#     )

# admin.site.register(User, CustomUserAdmin)
