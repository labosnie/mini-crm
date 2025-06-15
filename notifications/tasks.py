from celery import shared_task
from .services import NotificationService


@shared_task
def verifier_notifications():
    """Tâche planifiée pour vérifier les échéances et retards"""
    NotificationService.verifier_echeances()
    NotificationService.verifier_retards()
