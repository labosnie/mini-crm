from django.db import models
from clients.models import Client


class Projet(models.Model):
    STATUT_CHOICES = [
        ("en_cours", "En cours"),
        ("termine", "Terminé"),
        ("en_attente", "En attente"),
        ("annule", "Annulé"),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projets")
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="en_attente"
    )
    montant = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
