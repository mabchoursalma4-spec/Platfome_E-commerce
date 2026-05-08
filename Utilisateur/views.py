from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Utilisateur

@login_required
def espace_utilisateur(request):
    # verifier si c'est l'admin de la coopérative
    if request.user.is_staff:
        #  On récupère tous les clients inscrits(trie par date_joined )
        clients = Utilisateur.objects.filter(is_staff=False).order_by('-date_joined')
        
        return render(request, 'utilisateur/dashboard_admin.html', {
            'utilisateurs': clients,
            'titre': 'Gestion des Adhérents'
        })
    
    else:
        # si c'est un client On affiche ses propres données
        return render(request, 'utilisateur/profil.html', {
            'user': request.user,
            'titre': 'Mon Profil'
        })