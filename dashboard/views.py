from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import Client
from projets.models import Projet

# Create your views here.


@login_required
def dashboard(request):
    context = {
        "total_clients": Client.objects.count(),
        "total_projets": Projet.objects.count(),
        "projets_actifs": Projet.objects.filter(statut="en_cours").count(),
    }
    return render(request, "dashboard/dashboard.html", context)
