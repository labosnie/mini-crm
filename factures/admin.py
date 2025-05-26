from django.contrib import admin
from .models import Facture

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'projet', 'montant', 'date_emission', 'statut_paiement']
    list_filter = ['statut_paiement', 'date_emission']
    search_fields = ['numero', 'client__nom']
    


