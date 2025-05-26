from django.db import models
from clients.models import Client
from projets.models import Projet


class Facture(models.Model):
    """
    Représente une facture liée à un client et un projet
    """

    # Numéro unique de la facture
    numero = models.CharField(
        max_length=20,
        unique=True,
        help_text="Identifiant unique de la facture"
    )

    # Réference Client
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="factures",
        help_text="Client concerné par la facture"
    )

    # Réference Projet
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name="factures",
        help_text="Projet associé à la facture"
    )

    # Montant facturé
    montant = models.DecimalField(
        max_digits=10,   # nombre de chiffres maximum
        decimal_places=2, # Décimales
        help_text="Montant total de la facture (en euros)"
    )

    # Date d'émission automatique de la facture
    date_emission = models.DateTimeField(
        auto_now_add=True, # date fixée automatiquement à la création de la facture
        help_text="Date a laquelle la facture a été émise"
    )

    # Statut de paiement
    STATUT_CHOICES = [
        ("envoyée",   "Envoyée"),
        ("payée",     "Payée"),
        ("en_retard", "En retard"),
    ]
    statut_paiement = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="envoyee",
        help_text="Statut du paiement de la facture"
    )
    
    # Champ libre pour les remarques
    notes = models.TextField(
        blank=True,
        help_text="Remarques sur la facture, par exemple les motifs du retard de paiement"
    )
    
    def __str__(self):
        """
        Chaine de représentation dans l'admin et  ailleurs.
        """
        return f"Facture {self.numero} - {self.client.nom} - {self.projet}"

    def get_absolute_url(self):
        """
        URL canonique pour la vue détail de la facture.
        A adapter selon le nom de ta route.
        """
        from django.urls import reverse
        return reverse("detail_facture", args=[str(self.pk)])
    
    








