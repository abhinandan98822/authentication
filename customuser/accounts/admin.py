from django.contrib import admin
from.models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput,Textarea

# Register your models here.
# class Myadmin(admin.ModelAdmin):
    # list_display=('email','username','firstname','mobile')
    

admin.site.register(NewUser)

