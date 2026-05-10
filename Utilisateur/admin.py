from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'numero_tel',
        'adresse',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'numero_tel',
        'adresse',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('numero_tel', 'adresse')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('email', 'numero_tel', 'adresse')
        }),
    )