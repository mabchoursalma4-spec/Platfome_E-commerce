from django.urls import path
from . import views

urlpatterns = [
    path('', views.mes_commandes, name='mes_commandes'),
    path('<int:pk>/', views.detail_commande, name='detail_commande'),
]