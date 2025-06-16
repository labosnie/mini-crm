import os
import sys
import django
from datetime import datetime
from django.utils import timezone

# Configuration de l'environnement Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mini_crm.settings")
django.setup()

# Import des tâches
from factures.tasks import relancer_factures_en_retard
from notifications.services import NotificationService


def run_task():
    """Exécute les tâches planifiées"""
    print(f"Démarrage des tâches à {timezone.now()}")
    try:
        # Relance des factures
        print("Démarrage de la relance des factures...")
        relancer_factures_en_retard()
        print("Relance des factures terminée avec succès")

        # Vérification des notifications
        print("Démarrage de la vérification des notifications...")
        NotificationService.verifier_echeances()
        NotificationService.verifier_retards()
        print("Vérification des notifications terminée avec succès")

    except Exception as e:
        print(f"Erreur lors de l'exécution des tâches : {str(e)}")


if __name__ == "__main__":
    run_task()
