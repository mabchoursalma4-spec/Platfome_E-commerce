from django.urls import path
from . import views 

urlpatterns = [
    #acceuol
    path('', views.accueil, name='accueil'), 

   #catalogue complet
    path('catalogue/', views.liste_produits, name='catalogue'),

    # Détail d'un produit spécifique
    path('produit/<int:id>/', views.detail_produit, name='detail_produit'),
]