from django.urls import path
from . import views

app_name = "factures"

urlpatterns = [
    path(
        "", views.facture_list, name="facture_list"
    ),  # Liste des factures comme page d'accueil
    path("<int:pk>/", views.facture_detail, name="facture_detail"),
    path("nouvelle/", views.facture_create, name="facture_create"),
    path("<int:pk>/modifier/", views.facture_update, name="facture_update"),
    path("<int:pk>/supprimer/", views.facture_delete, name="facture_delete"),
    path(
        "<int:pk>/update-statut/",
        views.update_statut_facture,
        name="update_statut_facture",
    ),
    path("get-projets-client/", views.get_projets_client, name="get_projets_client"),
    path("export-csv/", views.export_csv, name="export_csv"),
    path("export-pdf/", views.export_pdf, name="export_pdf"),
    path("facture/<int:pk>/pdf/", views.telecharger_facture_pdf, name="facture_pdf"),
]
