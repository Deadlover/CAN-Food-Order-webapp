from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


class UserModelAdmin(BaseUserAdmin):
    list_display = ['date_joined','email','is_staff']
    list_filter = ('is_staff',)

    # after selecting the user
    fieldsets = (
        ('User Credentials',{'fields':['email','password']}),
        ('personal info',{'fields':['address','phone_number','first_name','last_name']}),
        ('User Permissions',{'fields':['is_staff']}),
    )

# set the paranthesis as it is cause it will occur error saying: TypeError: cannot unpack non-iterable NoneType object
    add_fieldsets = (
    (None, {  # You can provide a title instead of None if desired
        'classes': ['wide'],  # Ensure classes are correctly formatted
        'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff'),  # Include essential fields
    }),)



    ordering = ['email']  # Example ordering by email #** sort by email
    search_fields = ['email', 'first_name']  # search the word in email or firstname

admin.site.register(CustomUser, UserModelAdmin)