from django.db import models
from django.conf import settings

class Post(models.Model):
    STATUS = [('draft', 'Draft'), ('scheduled', 'Scheduled'), ('published', 'Published'), ('failed', 'Failed')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    content_variants = models.JSONField(default=dict, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    platforms = models.JSONField(default=list)
    error = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-scheduled_at', '-created_at']
    def __str__(self):
        return f"{self.content[:50]}... ({self.status})"
