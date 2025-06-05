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
    # Statistiques générales
    factures_impayees = Facture.objects.filter(statut_paiement="impayée").count()
    montant_impaye = (
        Facture.objects.filter(statut_paiement="impayée").aggregate(
            total=Sum("montant")
        )["total"]
        or 0
    )
    projets_en_cours = Projet.objects.filter(statut="en_cours").count()
    chiffre_affaire = (
        Facture.objects.filter(statut_paiement="payée").aggregate(total=Sum("montant"))[
            "total"
        ]
        or 0
    )

    # Micro-statistiques pour le CA
    debut_mois = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    debut_annee = datetime.now().replace(
        month=1, day=1, hour=0, minute=0, second=0, microsecond=0
    )

    ca_mois_precedent = (
        Facture.objects.filter(
            date_emission__gte=debut_mois, statut_paiement="payée"
        ).aggregate(total=Sum("montant"))["total"]
        or 0
    )

    ca_annee = (
        Facture.objects.filter(
            date_emission__gte=debut_annee, statut_paiement="payée"
        ).aggregate(total=Sum("montant"))["total"]
        or 0
    )

    # Micro-statistiques pour les factures
    date_limite = datetime.now() - timedelta(days=30)
    factures_en_retard = Facture.objects.filter(
        statut_paiement="impayée", date_echeance__lt=datetime.now()
    ).count()

    factures_payees_mois = Facture.objects.filter(
        statut_paiement="payée", date_emission__gte=debut_mois
    ).count()

    # Micro-statistiques pour les projets
    projets_termines = Projet.objects.filter(statut="termine").count()
    projets_en_attente = Projet.objects.filter(statut="en_attente").count()

    # Top 5 clients
    top_clients = Client.objects.annotate(
        total_factures=Count("factures"),
    ).order_by(
        "-total_factures"
    )[:5]

    # Evolution du CA sur 6 mois
    six_mois_avant = datetime.now() - timedelta(days=180)
    evolution_ca = (
        Facture.objects.filter(
            date_emission__gte=six_mois_avant, statut_paiement="payée"
        )
        .annotate(mois=TruncMonth("date_emission"))
        .values("mois")
        .annotate(total_ca=Sum("montant"))
        .order_by("mois")
    )

    # Préparation des données pour le graphique
    ca_labels = [item["mois"].strftime("%B %Y") for item in evolution_ca]
    ca_data = [float(item["total_ca"]) for item in evolution_ca]

    context = {
        "factures_impayees": factures_impayees,
        "montant_impaye": montant_impaye,
        "projets_en_cours": projets_en_cours,
        "chiffre_affaire": chiffre_affaire,
        "top_clients": top_clients,
        "ca_labels": json.dumps(ca_labels),
        "ca_data": json.dumps(ca_data),
        # Nouvelles statistiques
        "ca_mois_precedent": ca_mois_precedent,
        "ca_annee": ca_annee,
        "factures_en_retard": factures_en_retard,
        "factures_payees_mois": factures_payees_mois,
        "projets_termines": projets_termines,
        "projets_en_attente": projets_en_attente,
    }

    return render(request, "dashboard/dashboard.html", context)
