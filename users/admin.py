from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets+(('Additional Info',{'fields':('phone','picture','country')}),)
    add_fieldsets = UserAdmin.add_fieldsets+(('Additional Info',{'fields':('phone','picture','country')}),)
    list_display = ['username','email','phone','country']


