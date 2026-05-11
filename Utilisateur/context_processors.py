from django.db.models import Sum, Count
from django.utils import timezone


def admin_dashboard_stats(request):
    """
    Ajoute des statistiques personnalisées dans la page Django Admin.
    Ces données seront disponibles dans le template admin/index.html.
    """

    if not request.user.is_authenticated or not request.user.is_staff:
        return {}

    try:
        from .models import Utilisateur
        from Produits.models import Produit
        from Commande.models import Commande, LigneCommande

        today = timezone.now().date()
        debut_mois = today.replace(day=1)

        total_produits = Produit.objects.count()
        total_clients = Utilisateur.objects.filter(is_staff=False).count()
        total_commandes = Commande.objects.count()

        volume_total = Commande.objects.aggregate(
            total_volume=Sum('total_apres_reduction')
        )['total_volume'] or 0

        volume_mois = Commande.objects.filter(
            date_commande__gte=debut_mois
        ).aggregate(
            total_volume=Sum('total_apres_reduction')
        )['total_volume'] or 0

        produit_plus_commande = LigneCommande.objects.values(
            'produit__nom'
        ).annotate(
            total_quantite=Sum('quantite')
        ).order_by('-total_quantite').first()

        client_du_mois = Commande.objects.filter(
            date_commande__gte=debut_mois
        ).values(
            'client__username',
            'client__email'
        ).annotate(
            nombre_commandes=Count('num_commande')
        ).order_by('-nombre_commandes').first()

        return {
            'dashboard_total_produits': total_produits,
            'dashboard_total_clients': total_clients,
            'dashboard_total_commandes': total_commandes,
            'dashboard_volume_total': volume_total,
            'dashboard_volume_mois': volume_mois,
            'dashboard_produit_plus_commande': produit_plus_commande,
            'dashboard_client_du_mois': client_du_mois,
        }

    except Exception:
        return {}