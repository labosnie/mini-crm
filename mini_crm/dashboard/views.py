from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, F
from django.db.models.functions import TruncMonth
from factures.models import Facture
from projets.models import Projet
from clients.models import Client
from datetime import datetime, timedelta
from django.utils import timezone
import json
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard_views(request):
    # Statistiques générales
    factures_impayees = Facture.objects.filter(statut_paiement="impayée").count()
    montant_impaye = Facture.objects.filter(statut_paiement="impayée").aggregate(total=Sum("montant"))["total"] or 0
    projets_en_cours = Projet.objects.filter(statut="en_cours").count()
    chiffre_affaire = Facture.objects.filter(statut_paiement="payée").aggregate(total=Sum("montant"))["total"] or 0

    # KPIs mensuels
    now = timezone.now()
    debut_mois = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    debut_annee = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    # Chiffre d'affaires du mois
    ca_mois = Facture.objects.filter(
        date_emission__gte=debut_mois,
        statut_paiement="payée"
    ).aggregate(total=Sum("montant"))["total"] or 0

    # Chiffre d'affaires du mois précédent
    mois_precedent = debut_mois - timedelta(days=1)
    debut_mois_precedent = mois_precedent.replace(day=1)
    ca_mois_precedent = Facture.objects.filter(
        date_emission__gte=debut_mois_precedent,
        date_emission__lt=debut_mois,
        statut_paiement="payée"
    ).aggregate(total=Sum("montant"))["total"] or 0

    # Chiffre d'affaires de l'année
    ca_annee = Facture.objects.filter(
        date_emission__gte=debut_annee,
        statut_paiement="payée"
    ).aggregate(total=Sum("montant"))["total"] or 0

    # Nombre de factures émises ce mois
    factures_mois = Facture.objects.filter(
        date_emission__gte=debut_mois
    ).count()

    # Factures en retard
    factures_en_retard = Facture.objects.filter(
        statut_paiement="en_retard"
    ).count()

    # Factures payées ce mois
    factures_payees_mois = Facture.objects.filter(
        date_emission__gte=debut_mois,
        statut_paiement="payée"
    ).count()

    # Taux de conversion (factures payées / factures émises)
    taux_conversion = 0
    if factures_mois > 0:
        taux_conversion = (factures_payees_mois / factures_mois) * 100

    # Délai moyen de paiement
    delai_paiement = Facture.objects.filter(
        statut_paiement="payée",
        date_echeance__isnull=False
    ).aggregate(
        delai_moyen=Avg(
            F('date_echeance') - F('date_emission')
        )
    )["delai_moyen"] or timedelta(days=0)

    # Statistiques des projets
    projets_termines = Projet.objects.filter(statut="termine").count()
    projets_en_attente = Projet.objects.filter(statut="en_attente").count()

    # Top 5 clients
    top_clients = Client.objects.annotate(
        total_factures=Count("factures"),
        montant_total=Sum("factures__montant")
    ).order_by("-montant_total")[:5]

    # Évolution du CA sur 6 mois
    six_mois_avant = now - timedelta(days=180)
    evolution_ca = Facture.objects.filter(
        date_emission__gte=six_mois_avant,
        statut_paiement="payée"
    ).annotate(
        mois=TruncMonth("date_emission")
    ).values("mois").annotate(
        total_ca=Sum("montant")
    ).order_by("mois")

    logger.debug(f"Requête SQL: {evolution_ca.query}")
    logger.debug(f"Résultats bruts: {list(evolution_ca)}")

    # Préparation des données pour le graphique
    ca_labels = []
    ca_data = []
    
    # Dictionnaire pour la traduction des mois
    MOIS_FR = {
        1: 'Janvier', 2: 'Février', 3: 'Mars',
        4: 'Avril', 5: 'Mai', 6: 'Juin',
        7: 'Juillet', 8: 'Août', 9: 'Septembre',
        10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }
    
    # Créer un dictionnaire pour stocker les données par mois
    ca_par_mois = {}
    for item in evolution_ca:
        mois = item["mois"].month
        annee = item["mois"].year
        cle = f"{mois}/{annee}"
        ca_par_mois[cle] = float(item["total_ca"])
    
    logger.debug(f"Données par mois: {ca_par_mois}")
    
    # Remplir les 6 derniers mois, même s'il n'y a pas de données
    for i in range(6):
        date = now - timedelta(days=30*i)
        mois = date.month
        annee = date.year
        cle = f"{mois}/{annee}"
        ca_labels.insert(0, f"{MOIS_FR[mois]} {annee}")
        ca_data.insert(0, ca_par_mois.get(cle, 0.0))

    logger.debug(f"Labels finaux: {ca_labels}")
    logger.debug(f"Data finales: {ca_data}")

    # Vérification des données avant le JSON
    ca_labels_json = json.dumps(ca_labels, ensure_ascii=False)
    ca_data_json = json.dumps(ca_data)
    
    logger.debug(f"Labels JSON: {ca_labels_json}")
    logger.debug(f"Data JSON: {ca_data_json}")

    context = {
        # KPIs principaux
        "factures_impayees": factures_impayees,
        "montant_impaye": montant_impaye,
        "projets_en_cours": projets_en_cours,
        "chiffre_affaire": chiffre_affaire,
        
        # KPIs mensuels
        "ca_mois": ca_mois,
        "ca_mois_precedent": ca_mois_precedent,
        "ca_annee": ca_annee,
        "factures_mois": factures_mois,
        "factures_en_retard": factures_en_retard,
        "factures_payees_mois": factures_payees_mois,
        "taux_conversion": round(taux_conversion, 1),
        "delai_paiement": delai_paiement.days,
        
        # Statistiques des projets
        "projets_termines": projets_termines,
        "projets_en_attente": projets_en_attente,
        
        # Top clients
        "top_clients": top_clients,
        
        # Données pour le graphique
        "ca_labels": ca_labels_json,
        "ca_data": ca_data_json,
    }

    return render(request, "dashboard/dashboard.html", context)
