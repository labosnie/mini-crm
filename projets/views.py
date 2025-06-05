from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Projet
from .forms import ProjetForm

# Create your views here.


@login_required
def projet_list(request):
    projets = Projet.objects.all()
    return render(request, "projets/projet_list.html", {"projets": projets})


@login_required
def projet_detail(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    return render(request, "projets/projet_detail.html", {"projet": projet})


@login_required
def projet_create(request):
    if request.method == "POST":
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save()
            messages.success(request, "Projet créé avec succès.")
            return redirect("projets:projet_detail", pk=projet.pk)
    else:
        form = ProjetForm()
    return render(request, "projets/projet_form.html", {"form": form})


@login_required
def projet_update(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if request.method == "POST":
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet mis à jour avec succès.")
            return redirect("projets:projet_detail", pk=projet.pk)
    else:
        form = ProjetForm(instance=projet)
    return render(request, "projets/projet_form.html", {"form": form, "projet": projet})


@login_required
def projet_delete(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    if request.method == "POST":
        projet.delete()
        messages.success(request, "Projet supprimé avec succès.")
        return redirect("projets:projet_list")
    return render(request, "projets/projet_confirm_delete.html", {"projet": projet})
