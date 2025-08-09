from django.utils import timezone
from datetime import timedelta
from .models import Notification
from factures.models import Facture
from django.contrib.auth.models import User


class NotificationService:
    @staticmethod
    def creer_notification(user, type_notification, message, facture=None):
        return Notification.objects.create(
            user=user, type=type_notification, message=message, facture=facture
        )

    @staticmethod
    def verifier_echeances():
        """Vérifie les factures dont l'échéance approche"""
        date_limite = timezone.now().date() + timedelta(days=7)
        factures = Facture.objects.filter(
            date_echeance__lte=date_limite,
            date_echeance__gt=timezone.now().date(),
            statut_paiement="envoyée",
        )

        for facture in factures:
            jours_restants = (facture.date_echeance - timezone.now().date()).days
            message = f"La facture {facture.numero} arrive à échéance dans {jours_restants} jours"
            # Option A: notifier tous les staff
            staff_users = User.objects.filter(is_staff=True)
            for user in staff_users:
                NotificationService.creer_notification(
                    user, "ECHEANCE", message, facture
                )

    @staticmethod
    def verifier_retards():
        """Vérifie les factures en retard de paiement"""
        factures = Facture.objects.filter(
            date_echeance__lt=timezone.now().date(), statut_paiement="envoyée"
        )

        for facture in factures:
            jours_retard = (timezone.now().date() - facture.date_echeance).days
            message = (
                f"La facture {facture.numero} est en retard de {jours_retard} jours"
            )
            # Option A: notifier tous les staff
            staff_users = User.objects.filter(is_staff=True)
            for user in staff_users:
                NotificationService.creer_notification(
                    user, "RETARD", message, facture
                )
