from django.db import models
from django.contrib.auth.models import User
from factures.models import Facture


class Notification(models.Model):
    TYPE_CHOICES = [
        ("ECHEANCE", "Échéance de paiement"),
        ("RETARD", "Retard de paiement"),
        ("CREATION", "Nouvelle facture"),
        ("MODIFICATION", "Modification de facture"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facture = models.ForeignKey(
        Facture, on_delete=models.CASCADE, null=True, blank=True
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.type} - {self.message[:50]}"
