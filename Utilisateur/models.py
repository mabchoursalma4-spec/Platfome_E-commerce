from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    numero_tel = models.CharField(max_length=20, blank=True)
    adresse = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username

    def est_admin(self):
        return self.is_staff

    def est_client(self):
        return not self.is_staff