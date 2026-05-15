from django.shortcuts import render, get_object_or_404 , redirect
from .models import Produit, Categorie
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


#  ACCUEIL 
def accueil(request):
    return render(request, 'produits/accueil.html') 

# LISTE (Catalogue /boutique/)
def liste_produits(request):
    produits = Produit.objects.all()
    
    # 1. Filtre par recherche de nom
    query = request.GET.get('search')
    if query:
        produits = produits.filter(nom__icontains=query)
    
    # 2. Filtres par prix
    min_p = request.GET.get('min_price')
    max_p = request.GET.get('max_price')
    
    if min_p:
        produits = produits.filter(prix__gte=min_p) # gte = Greater Than or Equal
    if max_p:
        produits = produits.filter(prix__lte=max_p) # lte = Less Than or Equal

    return render(request, 'produits/liste.html', {
        'produits': produits,
        'query': query,
        'min_p': min_p,
        'max_p': max_p
    })

#  DETAIL (Page produit spécifique)
def detail_produit(request, id): 
    produit = get_object_or_404(Produit, id=id)
    return render(request, 'produits/detail.html', {'produit': produit})


@login_required(login_url='connexion')
def ajouter_au_panier(request, produit_id):
    # Initialiser le panier s'il n'existe pas
    panier = request.session.get('panier', {})
    
    # Ajouter le produit
    id_str = str(produit_id)
    if id_str in panier:
        panier[id_str] += 1
    else:
        panier[id_str] = 1
    
    # Sauvegarder
    request.session['panier'] = panier
    request.session.modified = True
    return redirect('voir_panier')

def voir_panier(request):
    panier_session = request.session.get('panier', {})
    produits_panier = []
    total_general = 0
    
    for p_id, quantite in panier_session.items():
        try:
            produit = Produit.objects.get(id=p_id)
            sous_total = produit.prix * quantite
            total_general += sous_total
            produits_panier.append({
                'produit': produit,
                'quantite': quantite,
                'sous_total': sous_total
            })
        except Produit.DoesNotExist:
            continue
            
    return render(request, 'produits/panier.html', {
        'panier': produits_panier,
        'total': total_general
    })

def supprimer_du_panier(request, produit_id):
    panier = request.session.get('panier', {})
    id_str = str(produit_id)
    if id_str in panier:
        del panier[id_str]
        request.session.modified = True
    return redirect('voir_panier')

def envoyer_confirmation_commande(user, panier, total):
    sujet = f"Confirmation de votre commande Titrit - #{user.id}2026"
    
    # On prépare les données pour le template d'email
    context = {
        'user': user,
        'panier': panier,
        'total': total,
    }
    
    # Version HTML de l'email (plus jolie)
    html_message = render_to_string('emails/confirmation_commande.html', context)
    # Version texte brut (sécurité)
    plain_message = strip_tags(html_message)
    
    destinataire = [user.email]
    expediteur = 'service-client@titrit.ma'

    send_mail(sujet, plain_message, expediteur, destinataire, html_message=html_message)

@login_required(login_url='connexion')
def valider_commande(request):
    panier_session = request.session.get('panier', {})
    
    if not panier_session:
        return redirect('liste_produits')

    produits_panier = []
    total_general = 0
    
    # 1. Reconstitution des données pour l'email et l'affichage
    for p_id, quantite in panier_session.items():
        try:
            produit = Produit.objects.get(id=p_id)
            sous_total = produit.prix * quantite
            total_general += sous_total
            produits_panier.append({
                'produit': produit,
                'quantite': quantite,
                'sous_total': sous_total
            })
        except Produit.DoesNotExist:
            continue

    # 2. Envoi de l'Email de Confirmation
    try:
        sujet = "Confirmation de votre commande - Titrit"
        destinataire = [request.user.email]
        expediteur = 'service-client@titrit.ma'
        
        context = {
            'user': request.user,
            'panier': produits_panier,
            'total': total_general,
        }
        
        html_message = render_to_string('emails/confirmation_commande.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            sujet, 
            plain_message, 
            expediteur, 
            destinataire, 
            html_message=html_message,
            fail_silently=True # Évite de bloquer la page si l'email échoue
        )
    except Exception as e:
        print(f"Erreur envoi email : {e}")

    # 3. VIDER LE PANIER (Important)
    request.session['panier'] = {}
    request.session.modified = True

    # 4. Redirection vers la page de succès
    return render(request, 'produits/succes.html', {
        'total': total_general
    })
