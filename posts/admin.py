from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_short', 'status', 'scheduled_at', 'created_at']
    list_filter = ['status', 'platforms']
    search_fields = ['content']
    def content_short(self, obj):
        return obj.content[:50]
