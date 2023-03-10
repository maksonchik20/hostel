from django.contrib import admin
from .models import CategoryRoom, HotelRoom, Client
from django.contrib.auth.admin import UserAdmin


class CustomClient(admin.ModelAdmin):
    model = Client
    list_display = ['first_name', 'last_name', 'surname', 'phone']
    fieldsets = (
        ( 
            None, 
            {
                'fields': 
                (
                    'first_name',
                    'last_name', 
                    'surname', 
                    'date_birthday',
                    'sex'
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


admin.site.register(Client, CustomClient)
admin.site.register(CategoryRoom)
admin.site.register(HotelRoom)




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
