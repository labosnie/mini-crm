from django.urls import path
from .views import societe_edit

urlpatterns = [
    path("societe/", societe_edit, name="societe_edit"),
]
