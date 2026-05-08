from django.core.management.base import BaseCommand
from Produits.models import Categorie, Produit


class Command(BaseCommand):
    help = "Insérer les produits Natus Marrakech avec prévisualisation avant insertion"

    def handle(self, *args, **kwargs):

        produits_par_categorie = {
            "Sun": [
                {
                    "nom": "Crème solaire visage SPF50 50 ml",
                    "description": "Crème solaire visage SPF50 pour protéger la peau contre les rayons du soleil.",
                    "prix": 140,
                    "stock": 25,
                },
                {
                    "nom": "Lait Solaire à l'huile d'Argan SPF 50 150 ml",
                    "description": "Lait solaire enrichi à l'huile d'argan pour une protection solaire du corps.",
                    "prix": 180,
                    "stock": 20,
                },
                {
                    "nom": "Huile bronzante Sèche à l'huile d'argan et de carotte SPF20 150ml",
                    "description": "Huile bronzante sèche à base d'huile d'argan et de carotte avec protection SPF20.",
                    "prix": 180,
                    "stock": 18,
                },
            ],

            "Parfums": [
                {
                    "nom": "Fleur d'Oranger - Eau de parfum 50ml",
                    "description": "Eau de parfum aux notes de fleur d'oranger.",
                    "prix": 250,
                    "stock": 15,
                },
                {
                    "nom": "Natus d'Orient - Eau de parfum 50ml",
                    "description": "Eau de parfum aux notes orientales.",
                    "prix": 250,
                    "stock": 15,
                },
                {
                    "nom": "Alia - Eau de parfum 50ml",
                    "description": "Eau de parfum féminine aux notes élégantes.",
                    "prix": 250,
                    "stock": 15,
                },
                {
                    "nom": "Lilia - Eau de parfum",
                    "description": "Eau de parfum aux notes florales.",
                    "prix": 250,
                    "stock": 15,
                },
            ],

            "Ambiance": [
                {
                    "nom": "Bougie Perlée Sans Parfum 1kg",
                    "description": "Bougie perlée sans parfum pour décoration et ambiance.",
                    "prix": 200,
                    "stock": 10,
                },
                {
                    "nom": "Bougie Perlée Parfumée Pot 300g",
                    "description": "Bougie perlée parfumée en pot pour créer une ambiance agréable.",
                    "prix": 150,
                    "stock": 12,
                },
                {
                    "nom": "Set 3 Verres pour bougie perlée",
                    "description": "Set de trois verres pour bougies perlées.",
                    "prix": 60,
                    "stock": 20,
                },
                {
                    "nom": "Huile à brûler 60ml",
                    "description": "Huile parfumée à brûler pour parfumer l'intérieur.",
                    "prix": 90,
                    "stock": 20,
                },
            ],

            "Corps": [
                {
                    "nom": "Gommage Eté à Marrakech Monoi et Coco",
                    "description": "Gommage corporel parfumé au monoï et coco.",
                    "prix": 70,
                    "stock": 30,
                },
                {
                    "nom": "Gelée moussante Miel, Huile Essentielle d'Orange et Huile d'Argan 200 ml",
                    "description": "Gelée moussante pour le corps au miel, orange et huile d'argan.",
                    "prix": 100,
                    "stock": 25,
                },
                {
                    "nom": "Douche exfoliante Moussante Huile d'Argan 200 ml",
                    "description": "Douche exfoliante moussante enrichie à l'huile d'argan.",
                    "prix": 100,
                    "stock": 25,
                },
                {
                    "nom": "Gel Douche à l'huile d'Argan",
                    "description": "Gel douche doux à base d'huile d'argan.",
                    "prix": 100,
                    "stock": 25,
                },
                {
                    "nom": "Mille vertus Huile d'Argan Cosmétique Pure 125 ml",
                    "description": "Huile d'argan cosmétique pure pour le soin de la peau et du corps.",
                    "prix": 180,
                    "stock": 18,
                },
                {
                    "nom": "Huile précieuse à l'huile d'argan 125ml",
                    "description": "Huile précieuse à base d'huile d'argan pour nourrir la peau.",
                    "prix": 144,
                    "stock": 18,
                },
                {
                    "nom": "Lait corporel hydratant à l'huile d'Argan 200ml",
                    "description": "Lait corporel hydratant enrichi à l'huile d'argan.",
                    "prix": 140,
                    "stock": 20,
                },
                {
                    "nom": "Lait Hydratant Corporel 200ml",
                    "description": "Lait hydratant corporel pour une peau douce et nourrie.",
                    "prix": 140,
                    "stock": 20,
                },
            ],

            "Hammam": [
                {
                    "nom": "Savon noir liquide à l'huile d'Argan, Nila et Miel - 200ml",
                    "description": "Savon noir liquide pour hammam à base d'huile d'argan, nila et miel.",
                    "prix": 100,
                    "stock": 25,
                },
            ],

            "Cheveux": [
                {
                    "nom": "Soin réparateur cheveux Huile d'Argan - Huile de Ricin - Huile essentielle de cèdre de l'Atlas 50ml",
                    "description": "Soin réparateur pour cheveux à base d'huile d'argan, ricin et cèdre de l'Atlas.",
                    "prix": 145,
                    "stock": 15,
                },
                {
                    "nom": "Sérum cheveux huile d'Argan et Romarin 30ml",
                    "description": "Sérum capillaire à l'huile d'argan et romarin.",
                    "prix": 100,
                    "stock": 20,
                },
                {
                    "nom": "Shampoing équilibrant verveine Usage fréquent 200ml",
                    "description": "Shampoing équilibrant à la verveine pour usage fréquent.",
                    "prix": 100,
                    "stock": 25,
                },
                {
                    "nom": "Sérum cheveux huile d'Argan et Romarin 200ml",
                    "description": "Sérum cheveux grand format à base d'huile d'argan et romarin.",
                    "prix": 190,
                    "stock": 15,
                },
                {
                    "nom": "Shampoing Fortifiant traitement à l'huile d'Argan Chute de cheveux, cheveux fatigués 200ml",
                    "description": "Shampoing fortifiant pour cheveux fatigués et chute de cheveux.",
                    "prix": 100,
                    "stock": 25,
                },
                {
                    "nom": "Shampoing équilibrant fleur d'oranger Usage fréquent 200ml",
                    "description": "Shampoing équilibrant à la fleur d'oranger pour usage fréquent.",
                    "prix": 100,
                    "stock": 25,
                },
                {
                    "nom": "Après shampoing démêlant à l'huile d'argan et beurre de karité 200 ML",
                    "description": "Après shampoing démêlant à l'huile d'argan et beurre de karité.",
                    "prix": 120,
                    "stock": 20,
                },
                {
                    "nom": "Huile antichute Huile d'Argan & huiles essentielles 100 ML",
                    "description": "Huile antichute à base d'huile d'argan et huiles essentielles.",
                    "prix": 168,
                    "stock": 15,
                },
            ],

            "Visage": [
                {
                    "nom": "Boite Have a beauty break - Aker fassi",
                    "description": "Coffret beauté Aker Fassi pour soin du visage.",
                    "prix": 290,
                    "stock": 10,
                },
                {
                    "nom": "Savon visage à l'huile d'argan et Safran 100g",
                    "description": "Savon visage enrichi à l'huile d'argan et au safran.",
                    "prix": 80,
                    "stock": 25,
                },
                {
                    "nom": "CREME PEELING ECLAT - Huile d'Argan & Extraits de Safran",
                    "description": "Crème peeling éclat pour visage à base d'huile d'argan et extraits de safran.",
                    "prix": 100,
                    "stock": 20,
                },
                {
                    "nom": "MOUSSE NETTOYANTE VISAGE - 100ml Huile d'Argan & Extraits de Safran",
                    "description": "Mousse nettoyante visage enrichie à l'huile d'argan et extraits de safran.",
                    "prix": 45,
                    "stock": 30,
                },
                {
                    "nom": "DEMAQUILLANT VISAGE 30ml - Huile d'Argan & Huile de Coco",
                    "description": "Démaquillant visage à base d'huile d'argan et huile de coco.",
                    "prix": 110,
                    "stock": 20,
                },
            ],

            "Protect": [
                {
                    "nom": "BAUME FONDANT A LEVRES Argan et Akerfassi 15ml",
                    "description": "Baume fondant pour lèvres à base d'argan et Aker Fassi.",
                    "prix": 75,
                    "stock": 25,
                },
                {
                    "nom": "BAUME MINE - 15ml Huile d'Argan et Poudre de coquelicot",
                    "description": "Baume mine avec huile d'argan et poudre de coquelicot.",
                    "prix": 115,
                    "stock": 20,
                },
                {
                    "nom": "GOMMAGE LEVRES - 15ml Huile d'argan, Sucre et Poudre de Coquelicot",
                    "description": "Gommage pour les lèvres à base d'huile d'argan, sucre et poudre de coquelicot.",
                    "prix": 75,
                    "stock": 20,
                },
            ],
        }

        # Prévisualisation avant insertion
        self.stdout.write(self.style.WARNING("\n--- PRODUITS À INSÉRER PAR CATÉGORIE ---"))

        total_produits = 0

        for nom_categorie, produits in produits_par_categorie.items():
            self.stdout.write(self.style.NOTICE(f"\nCatégorie : {nom_categorie}"))

            for produit in produits:
                total_produits += 1

                existe = Produit.objects.filter(
                    nom=produit["nom"],
                    categorie__nom=nom_categorie
                ).exists()

                statut = "existe déjà" if existe else "nouveau"

                self.stdout.write(
                    f"  - {produit['nom']} | {produit['prix']} DH | "
                    f"Stock : {produit['stock']} | {statut}"
                )

        self.stdout.write(self.style.WARNING(f"\nTotal produits à vérifier : {total_produits}"))

        confirmation = input("\nVoulez-vous insérer ces produits ? (oui/non) : ")

        if confirmation.lower() not in ["oui", "o", "yes", "y"]:
            self.stdout.write(self.style.ERROR("\nInsertion annulée."))
            return

        # Insertion dans la base
        produits_crees = 0
        produits_existants = 0

        for nom_categorie, produits in produits_par_categorie.items():

            categorie, created = Categorie.objects.get_or_create(
                nom=nom_categorie
            )

            for produit_data in produits:
                produit, created = Produit.objects.get_or_create(
                    nom=produit_data["nom"],
                    categorie=categorie,
                    defaults={
                        "description": produit_data["description"],
                        "prix": produit_data["prix"],
                        "stock": produit_data["stock"],
                    }
                )

                if created:
                    produits_crees += 1
                else:
                    produits_existants += 1

        self.stdout.write(self.style.SUCCESS("\nInsertion terminée avec succès."))
        self.stdout.write(self.style.SUCCESS(f"Produits créés : {produits_crees}"))
        self.stdout.write(self.style.WARNING(f"Produits déjà existants : {produits_existants}"))