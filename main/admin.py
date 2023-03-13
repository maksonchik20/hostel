from django.contrib import admin
from .models import CategoryRoom, HotelRoom, Client, Booking
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class CustomClient(admin.ModelAdmin):
    @admin.display(description='ФИО')
    def fio(self, obj):
        return ("%s %s %s" % (obj.last_name, obj.first_name, obj.surname))
    @admin.display(description='Пол')
    def pol(self, obj):
        if obj.sex == 'м':
            return "Мужской"
        else:
            return 'Женский'
    model = Client
    list_display = ['fio', 'phone', 'email']
    list_filter = ['sex', 'date_birthday']
    search_fields = ['first_name', 'last_name', 'surname', 'num_doc', 'phone', 'email']
    fieldsets = (
        ( 
            None, 
            {
                'fields': 
                (
                    'first_name',
                    'last_name', 
                    'surname', 
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
    

admin.site.register(Client, CustomClient)
admin.site.register(CategoryRoom)
admin.site.register(HotelRoom)
admin.site.register(Booking, BookingAdmin)




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
