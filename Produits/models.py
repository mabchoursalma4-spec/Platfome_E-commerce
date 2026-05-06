from django.db import models
from Utilisateur.models import Admin


class Categorie(models.Model):
    idCat = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    idProduit = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prix = models.FloatField(default=0)

    image = models.ImageField(upload_to='produits/', null=True, blank=True)
    stock = models.IntegerField(default=0)

    dateAjout = models.DateField(auto_now_add=True)
    dateModif = models.DateField(auto_now=True)
    dateSupp = models.DateField(null=True, blank=True)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produits'
    )

    admin = models.ForeignKey(
        Admin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produits_geres'
    )

    def __str__(self):
        return self.nom

    def diminuer_stock(self, quantite):
        if self.stock >= quantite:
            self.stock -= quantite
            self.save()
            return True
        return False

    def augmenter_stock(self, quantite):
        self.stock += quantite
        self.save()

    def verifier_stock(self, quantite=1):
        return self.stock >= quantite