from django.urls import path
from . import views 

urlpatterns = [
    #acceuol
    path('', views.accueil, name='accueil'), 
   path('panier/ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
   path('panier/', views.voir_panier, name='voir_panier'),
   #catalogue complet
    path('catalogue/', views.liste_produits, name='catalogue'),
    path('panier/supprimer/<int:produit_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    # Détail d'un produit spécifique
    path('produit/<int:id>/', views.detail_produit, name='detail_produit'),
    # URL pour traiter la commande (création en DB + Email)
    path('panier/valider/', views.valider_commande, name='valider_commande'),

    # URL pour afficher la page de succès finale
    path('commande/success/', views.valider_commande, name='succes_commande'),
]