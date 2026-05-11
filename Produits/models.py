from django.db import models
from django.utils import timezone
from django.conf import settings

#Modèle de Catégorie 
class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Modèle de Produit
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)
    prix = models.FloatField()
    stock = models.IntegerField()

    date_ajout = models.DateField(auto_now_add=True)
    date_modif = models.DateField(auto_now=True)
    date_supp = models.DateField(blank=True, null=True)
# relation avec la catégorie du produit
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produits'
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

    def verifier_stock(self):
        return self.stock > 0
    
    # Méthode pour obtenir la promotion active du produit
    """Cette méthode sert à chercher si le produit a une promotion active aujourd’hui."""
    def promotion_active(self):
        from django.utils import timezone

        today = timezone.now().date()

        return self.promotions.filter(
            date_debut__lte=today,
            date_fin__gte=today
        ).first()
    '''
    #Ce code est à mettre dans un template HTML 
    #Il sert à afficher la promotion active d’un produit, si elle existe.
    {% with promo=produit.promotion_active %}
    {% if promo %}
        <span class="badge-promo">-{{ promo.taux_reduction }}%</span>
        <p>{{ promo.description }}</p>
    {% endif %}
{% endwith %}
    '''


class Promotion(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    taux_reduction = models.FloatField()
    date_debut = models.DateField()
    date_fin = models.DateField()

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='promotions'
    )

    def __str__(self):
        return self.nom

    def verifier_validite(self):
        today = timezone.now().date()
        return self.date_debut <= today <= self.date_fin

    def prix_apres_promotion(self):
        if self.verifier_validite():
            return self.produit.prix - (self.produit.prix * self.taux_reduction / 100)
        return self.produit.prix
    