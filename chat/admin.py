from django.contrib import admin
from .models import Channel, Message


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'channel_type', 'created_by', 'created_at')
    list_filter = ('channel_type', 'created_at')
    search_fields = ('name', 'description', 'created_by__email', 'created_by__username')
    filter_horizontal = ('members',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'channel', 'message_type', 'created_at', 'is_deleted')
    list_filter = ('message_type', 'is_deleted', 'created_at')
    search_fields = ('content', 'author__email', 'author__username', 'channel__name')