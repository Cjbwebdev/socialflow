from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultAdmin
from .models import User

@admin.register(User)
class UserAdmin(DefaultAdmin):
    list_display = ['email', 'username', 'plan', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'plan']
