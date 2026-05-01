from django.contrib import admin
from .models import Channel, Message


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'channel_type',
        'created_by',
        'get_members',
        'created_at',
    )
    list_filter = ('channel_type', 'created_at')
    search_fields = (
        'name',
        'description',
        'created_by__email',
        'created_by__username',
        'members__email',
        'members__username',
    )
    filter_horizontal = ('members',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by').prefetch_related('members')

    @admin.display(description='Użytkownicy')
    def get_members(self, obj):
        members = obj.members.all()
        if not members:
            return '-'
        return ', '.join(user.username for user in members)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'channel',
        'message_type',
        'has_content',
        'has_image',
        'has_audio',
        'created_at',
        'is_deleted',
    )
    list_filter = ('message_type', 'is_deleted', 'created_at')
    search_fields = (
        'content',
        'author__email',
        'author__username',
        'channel__name',
    )
    ordering = ('-created_at',)
    list_select_related = ('author', 'channel')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'channel')

    @admin.display(boolean=True, description='Tekst')
    def has_content(self, obj):
        return bool(obj.content and obj.content.strip())

    @admin.display(boolean=True, description='Zdjęcie')
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(boolean=True, description='Audio')
    def has_audio(self, obj):
        return bool(obj.audio)