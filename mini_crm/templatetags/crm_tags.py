from django import template
from django.db.models import Count
from factures.models import Facture
from projets.models import Projet
from clients.models import Client

register = template.Library()


@register.simple_tag
def get_user_stats():
    factures_en_attente = Facture.objects.filter(statut_paiement="envoyée").count()
    projets_en_cours = Projet.objects.filter(statut="en_cours").count()
    clients_actifs = Client.objects.filter(projets__isnull=False).distinct().count()

    return {
        "factures_en_attente": factures_en_attente,
        "projets_en_cours": projets_en_cours,
        "clients_actifs": clients_actifs,
    }
