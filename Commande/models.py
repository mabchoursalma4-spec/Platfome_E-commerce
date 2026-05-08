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

    # Total avant réduction
    total = models.FloatField(default=0)

    # Pourcentage de réduction appliqué
    reduction = models.FloatField(default=0)

    # Total final après réduction
    total_apres_reduction = models.FloatField(default=0)

    statut = models.CharField(
        max_length=20,
        choices=StatutCommande.choices,
        default=StatutCommande.EN_ATTENTE
    )

    # Relation avec l'utilisateur qui a passé la commande
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commandes'
    )

    def __str__(self):
        return f"Commande {self.num_commande}"

    # Calcul de la quantité totale de produits dans la commande
    def calculer_quantite_totale(self):
        quantite_totale = 0

        for ligne in self.lignes.all():
            quantite_totale += ligne.quantite

        return quantite_totale

    # Calcul automatique de la réduction selon la quantité totale
    def calculer_reduction(self):
        quantite_totale = self.calculer_quantite_totale()

        if 5 <= quantite_totale < 10:
            return 2

        elif 10 <= quantite_totale <= 20:
            return 8

        elif quantite_totale > 20:
            return 10

        return 0

    # Calcul du total de la commande
    def calculer_total(self):
        total = 0

        for ligne in self.lignes.all():
            total += ligne.sous_total

        self.total = total

        # Application de la réduction
        self.reduction = self.calculer_reduction()

        montant_reduction = self.total * self.reduction / 100
        self.total_apres_reduction = self.total - montant_reduction

        self.save()

        return self.total_apres_reduction

    # Modification simple du statut sans email
    def modifier_statut_commande(self, statut):
        self.statut = statut
        self.save()
        return True

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

        # Recalcul automatique du total de la commande après ajout/modification d'une ligne
        self.commande.calculer_total()