from django.contrib import admin, messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Commande, LigneCommande, StatutCommande


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = (
        'prix_unitaire',
        'sous_total',
    )


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = (
        'num_commande',
        'client',
        'date_commande',
        'statut',
        'total',
        'reduction',
        'total_apres_reduction',
    )

    list_filter = (
        'statut',
        'date_commande',
    )

    search_fields = (
        'client__username',
        'client__email',
        'num_commande',
    )

    readonly_fields = (
        'date_commande',
        'total',
        'reduction',
        'total_apres_reduction',
    )

    inlines = [
        LigneCommandeInline,
    ]

    actions = [
        'valider_commandes',
        'annuler_commandes',
    ]

    def valider_commandes(self, request, queryset):
        commandes_validees = 0
        commandes_ignorees = 0

        for commande in queryset:
            if commande.statut == StatutCommande.VALIDEE:
                commandes_ignorees += 1
                continue

            stock_suffisant = True

            for ligne in commande.lignes.all():
                if ligne.produit.stock < ligne.quantite:
                    stock_suffisant = False
                    break

            if not stock_suffisant:
                self.message_user(
                    request,
                    f"Stock insuffisant pour la commande {commande.num_commande}.",
                    level=messages.ERROR
                )
                commandes_ignorees += 1
                continue

            for ligne in commande.lignes.all():
                produit = ligne.produit
                produit.stock -= ligne.quantite
                produit.save()

            commande.statut = StatutCommande.VALIDEE
            commande.calculer_total()
            commande.save()

            if commande.client.email:
                sujet = f"Confirmation de votre commande n°{commande.num_commande}"

                message = (
                    f"Bonjour {commande.client.first_name or commande.client.username},\n\n"
                    f"Votre commande n°{commande.num_commande} a été validée avec succès.\n\n"
                    f"Total avant réduction : {commande.total} DH\n"
                    f"Réduction appliquée : {commande.reduction}%\n"
                    f"Total à payer : {commande.total_apres_reduction} DH\n\n"
                    f"Merci pour votre confiance.\n\n"
                    f"L'équipe de la coopérative."
                )

                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [commande.client.email],
                    fail_silently=False,
                )

            commandes_validees += 1

        self.message_user(
            request,
            f"{commandes_validees} commande(s) validée(s). {commandes_ignorees} commande(s) ignorée(s).",
            level=messages.SUCCESS
        )

    valider_commandes.short_description = "Valider les commandes sélectionnées"

    def annuler_commandes(self, request, queryset):
        queryset.update(statut=StatutCommande.ANNULEE)

        self.message_user(
            request,
            "Les commandes sélectionnées ont été annulées.",
            level=messages.WARNING
        )

    annuler_commandes.short_description = "Annuler les commandes sélectionnées"


@admin.register(LigneCommande)
class LigneCommandeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'commande',
        'produit',
        'quantite',
        'prix_unitaire',
        'sous_total',
    )

    list_filter = (
        'produit',
    )

    search_fields = (
        'produit__nom',
        'commande__num_commande',
    )