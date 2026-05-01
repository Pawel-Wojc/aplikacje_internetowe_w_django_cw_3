from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email')
    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        ('Profil użytkownika', {
            'fields': ('avatar', 'bio')
        }),
    )