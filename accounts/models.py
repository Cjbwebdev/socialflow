from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    plan = models.CharField(max_length=20, default='free')
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.email or self.username
