from django.db import models
from Utilisateur.models import Client
from Produits.models import Produit
from notification.services import EmailService

#Enumération pour les statuts de commande
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
# relation avec le client qui a passé la commande
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='commandes'
    )

    def __str__(self):
        return f"Commande {self.num_commande}"
# modification du statut de la commande et envoi d'email de notification
    def modifier_statut_commande(self, statut):
        self.statut = statut
        self.save()

        if statut == StatutCommande.VALIDEE:
            EmailService.envoyer_confirmation_commande(
                self.client.email,
                self.num_commande
            )

        elif statut == StatutCommande.ANNULEE:
            EmailService.envoyer_annulation_commande(
                self.client.email,
                self.num_commande
            )

        return True
# calcul du total de la commande en fonction des lignes de commande
    def calculer_total(self):
        total = 0
        for ligne in self.lignes.all():
            total += ligne.sous_total

        self.total = total
        self.save()
        return total

    def annuler_commande(self):
        self.modifier_statut_commande(StatutCommande.ANNULEE)

# Modèle de Ligne de Commande
class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes'
    )
# relation avec le produit commandé
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

    def save(self, *args, **kwargs):
        self.prix_unitaire = self.produit.prix
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)