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

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        if request.user.has_perm('chat.can_soft_delete_message'):
            return (
                'author',
                'channel',
                'content',
                'message_type',
                'image',
                'audio',
                'created_at',
            )

        return (
            'author',
            'channel',
            'content',
            'message_type',
            'image',
            'audio',
            'created_at',
            'is_deleted',
        )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
            return

        if request.user.has_perm('chat.can_soft_delete_message') and change:
            original = Message.objects.get(pk=obj.pk)
            obj.author = original.author
            obj.channel = original.channel
            obj.content = original.content
            obj.message_type = original.message_type
            obj.image = original.image
            obj.audio = original.audio
            obj.created_at = original.created_at

        super().save_model(request, obj, form, change)