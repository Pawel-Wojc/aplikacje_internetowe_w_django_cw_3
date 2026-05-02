from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'id',
        'username',
        'email',
        'is_staff',
        'is_active',
        'is_blocked',
        'is_superuser',
    )
    list_filter = (
        'is_staff',
        'is_active',
        'is_blocked',
        'is_superuser',
        'groups',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Dane osobowe', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'bio')}),
        ('Status', {'fields': ('is_active', 'is_blocked', 'is_staff', 'is_superuser')}),
        ('Uprawnienia', {'fields': ('groups', 'user_permissions')}),
        ('Daty', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_blocked'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        if request.user.has_perm('accounts.can_block_user'):
            return (
                'username',
                'password',
                'first_name',
                'last_name',
                'email',
                'avatar',
                'bio',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'last_login',
                'date_joined',
            )

        return (
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'avatar',
            'bio',
            'is_active',
            'is_blocked',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'last_login',
            'date_joined',
        )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
            return

        if request.user.has_perm('accounts.can_block_user') and change:
            original = CustomUser.objects.get(pk=obj.pk)
            obj.username = original.username
            obj.password = original.password
            obj.first_name = original.first_name
            obj.last_name = original.last_name
            obj.email = original.email
            obj.avatar = original.avatar
            obj.bio = original.bio
            obj.is_active = original.is_active
            obj.is_staff = original.is_staff
            obj.is_superuser = original.is_superuser
            obj.last_login = original.last_login
            obj.date_joined = original.date_joined

        super().save_model(request, obj, form, change)