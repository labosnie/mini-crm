from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from .models import Facture
from .forms import FactureForm, StatutFactureForm
from projets.models import Projet
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime

# Create your views here.

@login_required
def facture_list(request):
    factures = Facture.objects.all()
    
    # Récupération des paramètres de filtrage
    search_query = request.GET.get('q', '').strip()
    client_id = request.GET.get('client', '').strip()
    statut = request.GET.get('statut', '').strip()
    date_debut = request.GET.get('date_debut', '').strip()
    date_fin = request.GET.get('date_fin', '').strip()

    # Filtrage par recherche textuelle
    if search_query:
        factures = factures.filter(
            Q(numero__icontains=search_query) |
            Q(client__nom__icontains=search_query) |
            Q(projet__titre__icontains=search_query)
        )

    # Filtrage par client
    if client_id:
        factures = factures.filter(client_id=client_id)

    # Filtrage par statut
    if statut:
        factures = factures.filter(statut_paiement=statut)

    # Filtrage par date
    if date_debut:
        factures = factures.filter(date_emission__gte=date_debut)
    if date_fin:
        factures = factures.filter(date_emission__lte=date_fin)

    # Tri par date d'émission décroissante
    factures = factures.order_by('-date_emission')

    # Pagination
    paginate_by = 10
    page = request.GET.get('page', 1)
    start = (int(page) - 1) * paginate_by
    end = start + paginate_by
    total_pages = (factures.count() + paginate_by - 1) // paginate_by

    context = {
        'factures': factures[start:end],
        'clients': Facture.objects.values_list('client', flat=True).distinct(),
        'statut_choices': Facture.STATUT_CHOICES,
        'is_paginated': True,
        'page_obj': {
            'number': int(page),
            'has_previous': int(page) > 1,
            'has_next': int(page) < total_pages,
            'previous_page_number': int(page) - 1,
            'next_page_number': int(page) + 1,
        },
        'paginator': {
            'page_range': range(1, total_pages + 1)
        }
    }
    
    return render(request, 'factures/facture_list.html', context)

@login_required
def facture_detail(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    return render(request, 'factures/facture_detail.html', {'facture': facture})

@login_required
def facture_create(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save()
            messages.success(request, 'Facture créée avec succès.')
            return redirect('factures:facture_detail', pk=facture.pk)
    else:
        form = FactureForm()
    return render(request, 'factures/facture_form.html', {'form': form})

@login_required
def facture_update(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            messages.success(request, 'Facture mise à jour avec succès.')
            return redirect('factures:facture_detail', pk=facture.pk)
    else:
        form = FactureForm(instance=facture)
    return render(request, 'factures/facture_form.html', {'form': form, 'facture': facture})

@login_required
def facture_delete(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        facture.delete()
        messages.success(request, 'Facture supprimée avec succès.')
        return redirect('factures:facture_list')
    return render(request, 'factures/facture_confirm_delete.html', {'facture': facture})

@login_required
def get_projets_client(request):
    client_id = request.GET.get('client_id')
    if not client_id:
        return JsonResponse([], safe=False)
    
    projets = Projet.objects.filter(client_id=client_id).values('id', 'titre')
    return JsonResponse(list(projets), safe=False)

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="factures_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Numéro', 'Client', 'Projet', 'Montant', 'Date d\'émission', 'Date d\'échéance', 'Statut'])
    
    factures = Facture.objects.all()
    
    # Application des filtres
    search_query = request.GET.get('q', '').strip()
    client_id = request.GET.get('client', '').strip()
    statut = request.GET.get('statut', '').strip()
    date_debut = request.GET.get('date_debut', '').strip()
    date_fin = request.GET.get('date_fin', '').strip()

    if search_query:
        factures = factures.filter(
            Q(numero__icontains=search_query) |
            Q(client__nom__icontains=search_query) |
            Q(projet__titre__icontains=search_query)
        )
    if client_id:
        factures = factures.filter(client_id=client_id)
    if statut:
        factures = factures.filter(statut_paiement=statut)
    if date_debut:
        factures = factures.filter(date_emission__gte=date_debut)
    if date_fin:
        factures = factures.filter(date_emission__lte=date_fin)
    
    for facture in factures:
        writer.writerow([
            facture.numero,
            facture.client.nom,
            facture.projet.titre,
            facture.montant,
            facture.date_emission.strftime('%d/%m/%Y'),
            facture.date_echeance.strftime('%d/%m/%Y') if facture.date_echeance else '-',
            facture.get_statut_paiement_display()
        ])
    
    return response

@login_required
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factures_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # En-tête
    data = [['Numéro', 'Client', 'Projet', 'Montant', 'Date d\'émission', 'Date d\'échéance', 'Statut']]
    
    # Données
    factures = Facture.objects.all()
    for facture in factures:
        data.append([
            facture.numero,
            facture.client.nom,
            facture.projet.titre,
            f"{facture.montant} €",
            facture.date_emission.strftime('%d/%m/%Y'),
            facture.date_echeance.strftime('%d/%m/%Y') if facture.date_echeance else '-',
            facture.get_statut_paiement_display()
        ])
    
    # Création du tableau
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    return response

@login_required
def update_statut_facture(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        form = StatutFactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            messages.success(request, f'Statut de la facture mis à jour : {facture.get_statut_paiement_display()}')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du statut')
    return redirect('factures:facture_detail', pk=facture.pk)
