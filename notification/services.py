from django.core.mail import send_mail
from django.conf import settings


class EmailService:
    """
    EmailService est une classe de service.
    Elle ne représente pas une table dans la base de données.
    Son rôle est d'envoyer des emails aux clients.
    """

    @staticmethod
    def envoyer_confirmation_commande(email_client, num_commande):
       
        #Envoyer un email au client lorsque sa commande est confirmée. 
        send_mail(
            subject="Confirmation de commande",
            message=f"Votre commande numéro {num_commande} a été confirmée avec succès.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_client],
            fail_silently=False,
        )

    @staticmethod
    def envoyer_annulation_commande(email_client, num_commande):

        #Envoyer un email au client lorsque sa commande est annulée.
        send_mail(
            subject="Annulation de commande",
            message=f"Votre commande numéro {num_commande} a été annulée.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_client],
            fail_silently=False,
        )

    @staticmethod
    def envoyer_email_promotion(email_client):
 
        #Envoyer un email au client pour l'informer d'une nouvelle promotion.
        send_mail(
            subject="Nouvelle promotion",
            message="Une nouvelle promotion est disponible sur notre plateforme.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_client],
            fail_silently=False,
        )