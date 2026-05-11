from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('mon-espace/', views.espace_utilisateur, name='espace_utilisateur'),
    #  Page d'inscription 
    path('inscription/', views.inscription, name='inscription'),

    # Page de connexion 
    path('connexion/', auth_views.LoginView.as_view(
        template_name='utilisateur/connexion.html', 
        redirect_authenticated_user=True      
    ), name='connexion'),

    # Page de déconnexion
    path('deconnexion/', auth_views.LogoutView.as_view(), name='deconnexion'),
]