from django.db import models
from django.conf import settings
from Produits.models import Produit



# Énumération pour les statuts de commande
class StatutCommande(models.TextChoices):
    EN_ATTENTE = 'EN_ATTENTE', 'En attente'
    VALIDEE = 'VALIDEE', 'Validée'
    EXPEDIEE = 'EXPEDIEE', 'Expédiée'
    ANNULEE = 'ANNULEE', 'Annulée'


# Modèle de Commande
class Commande(models.Model):
    num_commande = models.AutoField(primary_key=True)
    date_commande = models.DateField(auto_now_add=True)
    total = models.FloatField(default=0)

    statut = models.CharField(
        max_length=20,
        choices=StatutCommande.choices,
        default=StatutCommande.EN_ATTENTE
    )

    # Relation avec l'utilisateur qui a passé la commande
    # Si utilisateur.is_staff = False => c'est un client
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commandes'
    )

    def __str__(self):
        return f"Commande {self.num_commande}"


    # Calcul du total de la commande en fonction des lignes de commande
    def calculer_total(self):
        total = 0

        for ligne in self.lignes.all():
            total += ligne.sous_total

        self.total = total
        self.save()
        return total

    # Annulation de la commande
    def annuler_commande(self):
        self.modifier_statut_commande(StatutCommande.ANNULEE)


# Modèle de Ligne de Commande
class LigneCommande(models.Model):
    # Relation avec la commande
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    # Relation avec le produit commandé
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='lignes_commandes'
    )

    quantite = models.IntegerField()
    prix_unitaire = models.FloatField()
    sous_total = models.FloatField(default=0)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"

    # Calcul automatique du prix unitaire et du sous-total
    def save(self, *args, **kwargs):
        self.prix_unitaire = self.produit.prix
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)