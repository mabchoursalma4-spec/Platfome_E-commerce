from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Utilisateur
from .forms import InscriptionForm, ConnexionForm

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue au sein de la coopérative Titrit !")
            return redirect('accueil')
    else:
        form = InscriptionForm()
    # Chemin corrigé : utilisateur/ au lieu de users/
    return render(request, 'utilisateur/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accueil')
            else:
                messages.error(request, "Identifiants invalides.")
    else:
        form = ConnexionForm()
    # Chemin corrigé : utilisateur/ au lieu de users/
    return render(request, 'utilisateur/connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('accueil')

@login_required
def espace_utilisateur(request):
    if request.user.is_staff:
        # Récupération sans tri (order_by supprimé)
        clients = Utilisateur.objects.filter(is_staff=False)
        return render(request, 'utilisateur/dashboard_admin.html', {
            'utilisateurs': clients,
            'titre': 'Gestion des Adhérents'
        })
    else:
        return render(request, 'utilisateur/profil.html', {
            'user': request.user,
            'titre': 'Mon Profil'
        })