import os
import sys
import django
from datetime import datetime
from django.utils import timezone

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_crm.settings')
django.setup()

# Import de la tâche
from factures.tasks import relancer_factures_en_retard

def run_task():
    """Exécute la tâche de relance des factures"""
    print(f"Démarrage de la relance des factures à {timezone.now()}")
    try:
        relancer_factures_en_retard()
        print("Relance des factures terminée avec succès")
    except Exception as e:
        print(f"Erreur lors de la relance des factures : {str(e)}")

if __name__ == "__main__":
    run_task() 