from django.db import models
from Utilisateur.models import Client, Admin
from Produits.models import Produit


class Commande(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('CONFIRMEE', 'Confirmée'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
        ('RETOURNEE', 'Retournée'),
    ]

    numCommande = models.AutoField(primary_key=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='commandes'
    )

    admin = models.ForeignKey(
        Admin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commandes_gerees'
    )

    dateCommande = models.DateField(auto_now_add=True)

    statut = models.CharField(
        max_length=30,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE'
    )

    total = models.FloatField(default=0)

    def __str__(self):
        return f"Commande #{self.numCommande}"

    def calculer_total(self):
        total = 0
        for ligne in self.lignes.all():
            total += ligne.sousTotal
        self.total = total
        self.save()
        return total

    def annuler(self):
        self.statut = 'ANNULEE'
        self.save()


class LigneCommande(models.Model):
    idLigne = models.AutoField(primary_key=True)

    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='lignes_commande'
    )

    quantite = models.IntegerField(default=1)
    prixUnitaire = models.FloatField()
    sousTotal = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.sousTotal = self.quantite * self.prixUnitaire
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"