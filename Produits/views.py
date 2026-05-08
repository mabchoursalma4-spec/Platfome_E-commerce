from django.shortcuts import render, get_object_or_404
from .models import Produit, Categorie
from django.db.models import Count

# 1. ACCUEIL (Page beige avec cartes)
def accueil(request):
    return render(request, 'produits/accueil.html') 

# 2. LISTE (Catalogue /boutique/)
def liste_produits(request):
    categories = Categorie.objects.annotate(total=Count('produits'))
    produits = Produit.objects.all()

    # Filtre mot-clé
    mot_cle = request.GET.get('motcle')
    if mot_cle:
        produits = produits.filter(description__icontains=mot_cle)

    # Filtre catégorie (L'URL sera ?cat=ID)
    id_categorie = request.GET.get('cat')
    if id_categorie:
        produits = produits.filter(categorie_id=id_categorie)

    return render(request, 'produits/liste.html', {
        'produits': produits,
        'categories': categories
    })

# 3. DETAIL (Page produit spécifique)
# Changement de pk en id pour correspondre à ton urls.py
def detail_produit(request, id): 
    produit = get_object_or_404(Produit, id=id)
    # Je te conseille d'utiliser 'produit' comme nom de variable pour le HTML
    return render(request, 'produits/detail.html', {'produit': produit})