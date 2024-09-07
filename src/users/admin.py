from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','is_active','is_verified']

admin.site.register(User,UserAdmin)
