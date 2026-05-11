import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Platforme_ecommerce.settings')
django.setup()

from Produits.models import Produit

def lier_images():
    produits = Produit.objects.all()
    
    for produit in produits:
        nom_image = f"{produit.id}.jpeg" 
        chemin_relatif = f"produits/{nom_image}"
        
        if os.path.exists(os.path.join('media', chemin_relatif)):
            produit.image = chemin_relatif
            produit.save()
            print(f"✅ Image {nom_image} liée au produit : {produit.nom}")
        else:
            print(f"❌ Image {nom_image} introuvable pour le produit : {produit.nom}")

if __name__ == "__main__":
    lier_images()