from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    plan = models.CharField(max_length=20, default='free')
    stripe_customer_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.email or self.username


class SocialAccount(models.Model):
    PROVIDERS = [
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    provider_user_id = models.CharField(max_length=200)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, default='')
    expires_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'provider')

    def __str__(self):
        return f"{self.user} — {self.get_provider_display()}"
