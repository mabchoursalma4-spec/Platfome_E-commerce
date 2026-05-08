from django.core.management.base import BaseCommand
from Produits.models import Categorie


class Command(BaseCommand):
    help = "Insérer les catégories avec prévisualisation avant insertion"

    def handle(self, *args, **kwargs):

        # Liste des catégories inspirée du menu affiché dans l'image
        categories_data = [
            "Idées cadeaux",
            "Visage",
            "Corps",
            "Cheveux",
            "Hammam",
            "Ambiance",
            "Desert",
            "Homme",
            "Enfant",
            "Parfums",
            "Sun",
            "Protect",
            "Voyage",
            "Gourmet",
            "Produits d'Accueil",
            "Format Professionnel",
        ]

        # Affichage des catégories avant insertion
        self.stdout.write(self.style.WARNING("\n--- CATÉGORIES À INSÉRER ---"))

        for index, nom in enumerate(categories_data, start=1):
            existe = Categorie.objects.filter(nom=nom).exists()

            if existe:
                statut = "existe déjà"
            else:
                statut = "nouvelle"

            self.stdout.write(f"{index}. {nom}  [{statut}]")

        # Confirmation avant insertion
        confirmation = input("\nVoulez-vous insérer ces catégories ? (oui/non) : ")

        if confirmation.lower() not in ["oui", "o", "yes", "y"]:
            self.stdout.write(self.style.ERROR("\nInsertion annulée."))
            return

        # Insertion dans la base
        compteur_creation = 0
        compteur_existant = 0

        for nom in categories_data:
            categorie, created = Categorie.objects.get_or_create(nom=nom)

            if created:
                compteur_creation += 1
            else:
                compteur_existant += 1

        self.stdout.write(self.style.SUCCESS("\nInsertion terminée avec succès."))
        self.stdout.write(self.style.SUCCESS(f"Catégories créées : {compteur_creation}"))
        self.stdout.write(self.style.WARNING(f"Catégories déjà existantes : {compteur_existant}"))