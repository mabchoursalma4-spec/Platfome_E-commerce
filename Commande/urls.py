from django.urls import path
from . import views

urlpatterns = [
    path('', views.mes_commandes, name='mes_commandes'),
    path('<int:num_commande>/', views.detail_commande, name='detail_commande'),
    path('<int:num_commande>/envoyer-email/', views.envoyer_email_service, name='envoyer_email_service'),
]