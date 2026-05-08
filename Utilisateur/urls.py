from django.urls import path
from . import views

urlpatterns = [
    path('mon-espace/', views.espace_utilisateur, name='espace_utilisateur'),
]