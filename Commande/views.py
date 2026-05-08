from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Commande, LigneCommande

@login_required
def mes_commandes(request):
  
    #Affiche l'historique de toutes les demandes du client.
    commandes = Commande.objects.filter(client_id=request.user.id).order_by('-date_commande')
    return render(request, 'commande/liste_des_commandes.html', {'commandes': commandes})

@login_required
def detail_commande(request, num_commande):
    #ligne de commande
    commande = get_object_or_404(Commande, num_commande=num_commande, client_id=request.user.id)
    # Récupération des produits liés à cette commande via la table LigneCommande
    lignes = LigneCommande.objects.filter(commande=commande)
    
    return render(request, 'commande/detail.html', {
        'commande': commande,
        'lignes': lignes
    })

@login_required
def envoyer_email_service(request, num_commande):
   
    #Action déclenchée pour envoyer le récapitulatif au client.
  
    commande = get_object_or_404(Commande, num_commande=num_commande, client_id=request.user.id)
    lignes = LigneCommande.objects.filter(commande=commande)
    
    # Construction de la liste des produits pour l'email
    detail_produits = ""
    for item in lignes:
        detail_produits += f"- {item.produit.nom} | Qté : {item.quantite} | Prix : {item.prix_unitaire} DT\n"

    # Envoi de l'email  au client
    sujet = f"Votre demande de cosmétiques n°{commande.num_commande}"
    message = (
        f"Bonjour {request.user.first_name},\n\n"
        f"Nous avons bien reçu votre sélection de produits artisanaux.\n\n"
        f"Récapitulatif :\n{detail_produits}\n"
        f"Total estimé : {commande.total} DT\n\n"
        f"Un artisan de la coopérative vous contactera bientôt.\n\n"
        f"Cordialement,\nL'équipe de la Coopérative."
    )

    
    send_mail(sujet, message, 'titritcooperative@gmail.com', [request.user.email])

    # Mise à jour du statut dans ta table Commande
    commande.statut = "Email envoyé au client"
    commande.save()

    # Redirection vers le détail avec un message de succès
    return redirect('detail_commande', num_commande=commande.num_commande)