from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client, Interaction, Tag
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy, reverse
from django.db.models import Q
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class ClientListViews(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 10

    def get_queryset(self):
        qs = Client.objects.all()

        # Récuperatiuon des paramètres de filtrage
        search_query = self.request.GET.get("q", "").strip()
        statut = self.request.GET.get("statut", "").strip()
        ville = self.request.GET.get("ville", "").strip()
        date_debut = self.request.GET.get("date_debut", "").strip()
        date_fin = self.request.GET.get("date_fin", "").strip()

        if search_query:
            qs = qs.filter(
                Q(nom__icontains=q)
                | Q(email__icontains=q)
                | Q(prenom__icontains=q)
                | Q(ville__icontains=q)
            )

        # Filtrage par statut
        if statut:
            qs = qs.filter(statut=statut)

        # Filtrage par ville
        if ville:
            qs = qs.filter(ville__iexact=ville)

        # Filtrage par date
        if date_debut:
            qs = qs.filter(date_creation__gte=date_debut)
        if date_fin:
            qs = qs.filter(date_creation__lte=date_fin)

        return qs.order_by("-date_creation")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["statut_filter"] = self.request.GET.get("statut", "")
        context["statut_choices"] = Client.STATUT_CHOICES
        return context


class ClientDetailViews(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_detail.html"


class ClientCreateViews(LoginRequiredMixin, CreateView):
    model = Client
    fields = [
        "nom",
        "prenom",
        "email",
        "telephone",
        "adresse",
        "ville",
        "code_postal",
        "pays",
        "statut",
        "notes",
    ]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")

    def form_valid(self, form):
        messages.success(self.request, "Client créé avec succès.")
        return super().form_valid(form)


class ClientUpdateViews(LoginRequiredMixin, UpdateView):
    model = Client
    fields = [
        "nom",
        "prenom",
        "email",
        "telephone",
        "adresse",
        "ville",
        "code_postal",
        "pays",
        "statut",
        "notes",
        "tags",
    ]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Client mis à jour avec succès.")
        return super().form_valid(form)


class ClientDeleteViews(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("clients:client_list")


class ClientExportView(LoginRequiredMixin, View):
    def get(self, request, format_type):
        if format_type == "csv":
            return self.export_csv()
        elif format_type == "pdf":
            return self.export_pdf()
        return HttpResponseBadRequest("Format non supporté")

    def export_csv(self):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="clients.csv"'

        writer = csv.writer(response)
        writer.writerow(["Nom", "Prénom", "Email", "Téléphone", "Ville", "Statut"])

        clients = Client.objects.all()
        for client in clients:
            writer.writerow(
                [
                    client.nom,
                    client.prenom,
                    client.email,
                    client.telephone,
                    client.ville,
                    client.get_statut_display(),
                ]
            )

        return response

    def export_pdf(self):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="clients.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # En-tête
        data = [["Nom", "Prénom", "Email", "Téléphone", "Ville", "Statut"]]

        # Données
        clients = Client.objects.all()
        for client in clients:
            data.append(
                [
                    client.nom,
                    client.prenom,
                    client.email,
                    client.telephone,
                    client.ville,
                    client.get_statut_display(),
                ]
            )

        # Création du tableau
        table = Table(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        elements.append(table)
        doc.build(elements)
        return response


class InteractionCreateView(LoginRequiredMixin, CreateView):
    model = Interaction
    fields = ["type", "description"]
    template_name = "clients/interaction_form.html"

    def form_valid(self, form):
        form.instance.client_id = self.kwargs["client_id"]
        form.instance.utilisateur = self.request.user
        messages.success(self.request, "Interaction enregistrée avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("clients:client_detail", kwargs={"pk": self.kwargs["client_id"]})
