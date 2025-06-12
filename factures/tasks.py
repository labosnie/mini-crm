from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Facture

def relancer_factures_en_retard():
    """
    Fonction qui identifie et relance les factures en retard.
    Une facture est considérée en retard si :
    - Son statut est 'envoyée'
    - Sa date d'échéance est dépassée
    """
    # Récupérer toutes les factures en retard
    factures_en_retard = Facture.objects.filter(
        statut_paiement='envoyée',
        date_echeance__lt=timezone.now().date()
    )

    for facture in factures_en_retard:
        # Mettre à jour le statut de la facture
        facture.statut_paiement = 'en_retard'
        facture.save()

        # Envoyer un email de relance
        sujet = f"Relance de facture {facture.numero}"
        message = f"""
        Bonjour {facture.client.nom},

        Nous vous rappelons que la facture {facture.numero} d'un montant de {facture.montant}€ 
        est en retard de paiement depuis le {facture.date_echeance}.

        Merci de bien vouloir procéder au règlement dans les plus brefs délais.

        Cordialement,
        L'équipe de facturation
        """

        # Envoyer l'email
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [facture.client.email],
            fail_silently=False,
        ) 