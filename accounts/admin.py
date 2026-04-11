from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultAdmin
from .models import User, SocialAccount

@admin.register(User)
class UserAdmin(DefaultAdmin):
    list_display = ['email', 'username', 'plan', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'plan']

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'provider_user_id', 'expires_at', 'created_at']
    list_filter = ['provider']
    search_fields = ['user__username', 'user__email', 'provider_user_id']
