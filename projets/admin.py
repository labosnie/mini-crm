from django.contrib import admin
from .models import Projet


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ("titre", "client", "date_debut", "date_fin", "statut", "montant")
    list_filter = ("statut", "date_debut", "client")
    search_fields = ("titre", "description", "client__nom")
    date_hierarchy = "date_debut"
    ordering = ("-date_debut",)
