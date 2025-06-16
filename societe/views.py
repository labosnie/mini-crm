from django.shortcuts import render, redirect
from .models import Societe
from .forms import SocieteForm


def societe_edit(request):
    societe, _ = Societe.objects.get_or_create(pk=1)  # Un seul profil société
    if request.method == "POST":
        form = SocieteForm(request.POST, instance=societe)
        if form.is_valid():
            form.save()
            return redirect("societe_edit")
    else:
        form = SocieteForm(instance=societe)
    return render(request, "societe/edit.html", {"form": form})
