from django.db import models


class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=191, unique=True)
    numero_tel = models.CharField(max_length=20)
    motdepasse = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Client(Utilisateur):
    adresse = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Admin(Utilisateur):
    def __str__(self):
        return self.nom