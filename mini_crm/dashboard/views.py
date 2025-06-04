from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from factures.models import Facture
from projets.models import Projet
from clients.models import Client
from datetime import datetime, timedelta
import json


@login_required
def dashboard_views(request):
    # Statistiques génerales
    factures_impayees = Facture.objects.filter(statut_paiement='impayée').count()
    montant_impaye = Facture.objects.filter(statut_paiement='impayée').aggregate(total=Sum('montant'))['total'] or 0
    projets_en_cours = Projet.objects.filter(statut='en_cours').count()
    chiffre_affaire = Facture.objects.filter(statut_paiement='payée').aggregate(total=Sum('montant'))['total'] or 0

    # Top 5 clients
    top_clients = Client.objects.annotate(
        total_factures=Count('factures'),
    ).order_by('-total_factures')[:5]

    # Evolution du CA sur 6 mois
    six_mois_avant = datetime.now() - timedelta(days=180)
    evolution_ca = Facture.objects.filter(
        date_emission__gte=six_mois_avant,
        statut_paiement='payée'
    ).annotate(
        mois=TruncMonth('date_emission')
    ).values('mois').annotate(
        total_ca=Sum('montant')
    ).order_by('mois')

    # Préparation des données pour le graphique
    ca_labels = [item['mois'].strftime('%B %Y') for item in evolution_ca]
    ca_data = [float(item['total_ca']) for item in evolution_ca]

    context = {
        'factures_impayees': factures_impayees,
        'montant_impaye': montant_impaye,
        'projets_en_cours': projets_en_cours,
        'chiffre_affaire': chiffre_affaire,
        'top_clients': top_clients,
        'ca_labels': json.dumps(ca_labels),
        'ca_data': json.dumps(ca_data),
    }

    return render(request, 'dashboard/dashboard.html', context)
