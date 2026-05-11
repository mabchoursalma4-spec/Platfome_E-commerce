from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Administration de la Coopérative"
admin.site.site_title = "Admin Coopérative"
admin.site.index_title = "Tableau de bord"

# Enlever le menu latéral gauche de Django Admin
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('Produits.urls')),
    path('commandes/', include('Commande.urls')),
    path('utilisateur/', include('Utilisateur.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)