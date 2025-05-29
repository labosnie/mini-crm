from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Facture
from .forms import FactureForm
from projets.models import Projet

# Create your views here.

@login_required
def facture_list(request):
    factures = Facture.objects.all()
    return render(request, 'factures/facture_list.html', {'factures': factures})

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
    projets = Projet.objects.filter(client_id=client_id).values('id', 'titre')
    return JsonResponse(list(projets), safe=False)
