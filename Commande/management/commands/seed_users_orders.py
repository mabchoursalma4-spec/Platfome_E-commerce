from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

from Produits.models import Produit
from Commande.models import Commande, LigneCommande, StatutCommande


class Command(BaseCommand):
    help = "Générer des utilisateurs, commandes et lignes de commande avec confirmation avant insertion"

    def handle(self, *args, **kwargs):
        fake = Faker("fr_FR")
        User = get_user_model()

        # Nombre de données à générer
        nombre_clients = 8
        nombre_commandes = 12

        # Vérifier s'il existe des produits
        produits_existants = list(Produit.objects.all())

        if not produits_existants:
            self.stdout.write(self.style.ERROR(
                "Aucun produit trouvé. Insère d'abord les produits avant de créer des commandes."
            ))
            return

        # =========================
        # 1. Générer les clients fake
        # =========================

        clients_data = []

        for i in range(nombre_clients):
            prenom = fake.first_name()
            nom = fake.last_name()

            username = f"{prenom.lower()}.{nom.lower()}{random.randint(100, 999)}"
            email = f"{username}@test.com"

            clients_data.append({
                "username": username,
                "first_name": prenom,
                "last_name": nom,
                "email": email,
                "numero_tel": fake.phone_number(),
                "adresse": fake.address().replace("\n", ", "),
                "is_staff": False,
                "is_superuser": False,
                "password": "1234",
            })

        # =========================
        # 2. Générer les commandes fake
        # =========================

        commandes_data = []

        for i in range(nombre_commandes):
            client_index = random.randint(0, nombre_clients - 1)

            nombre_lignes = random.randint(1, 4)

            lignes = []

            produits_choisis = random.sample(
                produits_existants,
                min(nombre_lignes, len(produits_existants))
            )

            for produit in produits_choisis:
                quantite = random.randint(1, 8)

                lignes.append({
                    "produit": produit,
                    "quantite": quantite,
                    "prix_unitaire": produit.prix,
                    "sous_total": produit.prix * quantite,
                })

            total_commande = sum(ligne["sous_total"] for ligne in lignes)
            quantite_totale = sum(ligne["quantite"] for ligne in lignes)

            if 5 <= quantite_totale < 10:
                reduction = 2
            elif 10 <= quantite_totale <= 20:
                reduction = 8
            elif quantite_totale > 20:
                reduction = 10
            else:
                reduction = 0

            total_apres_reduction = total_commande - (total_commande * reduction / 100)

            commandes_data.append({
                "client_index": client_index,
                "statut": random.choice([
                    StatutCommande.EN_ATTENTE,
                    StatutCommande.VALIDEE,
                    StatutCommande.EXPEDIEE,
                    StatutCommande.ANNULEE,
                ]),
                "lignes": lignes,
                "quantite_totale": quantite_totale,
                "total": total_commande,
                "reduction": reduction,
                "total_apres_reduction": total_apres_reduction,
            })

        # =========================
        # 3. Prévisualisation avant insertion
        # =========================

        self.stdout.write(self.style.WARNING("\n========== CLIENTS À INSÉRER ==========\n"))

        for index, client in enumerate(clients_data, start=1):
            existe = User.objects.filter(username=client["username"]).exists()

            statut = "existe déjà" if existe else "nouveau"

            self.stdout.write(
                f"{index}. {client['username']} | {client['email']} | "
                f"{client['numero_tel']} | Client | {statut}"
            )

        self.stdout.write(self.style.WARNING("\n========== COMMANDES À INSÉRER ==========\n"))

        for index, commande in enumerate(commandes_data, start=1):
            client = clients_data[commande["client_index"]]

            self.stdout.write(self.style.NOTICE(
                f"\nCommande {index} | Client : {client['username']} | "
                f"Statut : {commande['statut']}"
            ))

            for ligne in commande["lignes"]:
                self.stdout.write(
                    f"   - Produit : {ligne['produit'].nom} | "
                    f"Qté : {ligne['quantite']} | "
                    f"Prix : {ligne['prix_unitaire']} DH | "
                    f"Sous-total : {ligne['sous_total']} DH"
                )

            self.stdout.write(
                f"   Quantité totale : {commande['quantite_totale']} | "
                f"Total : {commande['total']:.2f} DH | "
                f"Réduction : {commande['reduction']}% | "
                f"Total final : {commande['total_apres_reduction']:.2f} DH"
            )

        # =========================
        # 4. Confirmation
        # =========================

        confirmation = input("\nVoulez-vous insérer ces données dans la base ? (oui/non) : ")

        if confirmation.lower() not in ["oui", "o", "yes", "y"]:
            self.stdout.write(self.style.ERROR("\nInsertion annulée."))
            return

        # =========================
        # 5. Insertion dans la base
        # =========================

        clients_crees = []

        for client_data in clients_data:
            utilisateur, created = User.objects.get_or_create(
                username=client_data["username"],
                defaults={
                    "email": client_data["email"],
                    "first_name": client_data["first_name"],
                    "last_name": client_data["last_name"],
                    "numero_tel": client_data["numero_tel"],
                    "adresse": client_data["adresse"],
                    "is_staff": client_data["is_staff"],
                    "is_superuser": client_data["is_superuser"],
                }
            )

            if created:
                utilisateur.set_password(client_data["password"])
                utilisateur.save()

            clients_crees.append(utilisateur)

        commandes_creees = 0
        lignes_creees = 0

        for commande_data in commandes_data:
            client = clients_crees[commande_data["client_index"]]

            commande = Commande.objects.create(
                client=client,
                statut=commande_data["statut"],
            )

            for ligne_data in commande_data["lignes"]:
                LigneCommande.objects.create(
                    commande=commande,
                    produit=ligne_data["produit"],
                    quantite=ligne_data["quantite"],
                )

                lignes_creees += 1

            # Calcul automatique total + réduction
            commande.calculer_total()

            commandes_creees += 1

        self.stdout.write(self.style.SUCCESS("\nInsertion terminée avec succès."))
        self.stdout.write(self.style.SUCCESS(f"Clients créés : {len(clients_crees)}"))
        self.stdout.write(self.style.SUCCESS(f"Commandes créées : {commandes_creees}"))
        self.stdout.write(self.style.SUCCESS(f"Lignes de commande créées : {lignes_creees}"))
        self.stdout.write(self.style.WARNING("Mot de passe des clients fake : 1234"))