from django.contrib import admin
from .models import Categorie, Produit, Promotion


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nom',
        'categorie',
        'prix',
        'stock',
        'date_ajout',
        'date_modif',
    )

    list_filter = (
        'categorie',
        'date_ajout',
    )

    search_fields = (
        'nom',
        'description',
    )

    list_editable = (
        'prix',
        'stock',
    )

    readonly_fields = (
        'date_ajout',
        'date_modif',
    )

    fieldsets = (
        ('Informations du produit', {
            'fields': (
                'nom',
                'description',
                'image',
                'categorie',
            )
        }),

        ('Prix et stock', {
            'fields': (
                'prix',
                'stock',
            )
        }),

        ('Dates', {
            'fields': (
                'date_ajout',
                'date_modif',
                'date_supp',
            )
        }),
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nom',
        'produit',
        'taux_reduction',
        'date_debut',
        'date_fin',
    )

    list_filter = (
        'date_debut',
        'date_fin',
        'produit',
    )

    search_fields = (
        'nom',
        'description',
        'produit__nom',
    )