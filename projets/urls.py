from django.urls import path
from . import views

app_name = "projets"

urlpatterns = [
    path("", views.projet_list, name="projet_list"),
    path("<int:pk>/", views.projet_detail, name="projet_detail"),
    path("nouveau/", views.projet_create, name="projet_create"),
    path("<int:pk>/modifier/", views.projet_update, name="projet_update"),
    path("<int:pk>/supprimer/", views.projet_delete, name="projet_delete"),
]
