from django.db import models
from Utilisateur.models import Client
from Produits.models import Produit


class Panier(models.Model):
    idPanier = models.AutoField(primary_key=True)

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name='panier'
    )

    def __str__(self):
        return f"Panier de {self.client.nom}"

    def calculer_total(self):
        total = 0
        for ligne in self.lignes.all():
            total += ligne.produit.prix * ligne.quantite
        return total


class LignePanier(models.Model):
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='lignes_panier'
    )

    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"