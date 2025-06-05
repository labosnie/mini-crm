from django.db import models
from clients.models import Client
from projets.models import Projet
from django.utils import timezone


class Facture(models.Model):
    """
    Représente une facture liée à un client et un projet
    """

    # Numéro unique de la facture
    numero = models.CharField(
        max_length=20, unique=True, help_text="Identifiant unique de la facture"
    )

    # Réference Client
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="factures",
        help_text="Client concerné par la facture",
    )

    # Réference Projet
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name="factures",
        help_text="Projet associé à la facture",
    )

    # Montant facturé
    montant = models.DecimalField(
        max_digits=10,  # nombre de chiffres maximum
        decimal_places=2,  # Décimales
        help_text="Montant total de la facture (en euros)",
    )

    # Date d'émission automatique de la facture
    date_emission = models.DateTimeField(
        auto_now_add=True,  # date fixée automatiquement à la création de la facture
        help_text="Date a laquelle la facture a été émise",
    )

    # Date d'échéance de paiement
    date_echeance = models.DateField(
        null=True, blank=True, help_text="Date limite de paiement"
    )

    # Statut de paiement
    STATUT_CHOICES = [
        ("envoyée", "Envoyée"),
        ("payée", "Payée"),
        ("en_retard", "En retard"),
        ("annulée", "Annulée"),
        ("brouillon", "Brouillon"),
    ]
    statut_paiement = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="envoyee",
        help_text="Statut du paiement de la facture",
    )

    # Champ libre pour les remarques
    notes = models.TextField(
        blank=True,
        help_text="Remarques sur la facture, par exemple les motifs du retard de paiement",
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

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.generer_numero()
        super().save(*args, **kwargs)

    def generer_numero(self):
        """
        Génère un numéro de facture unique au format ANNEE-NUMERO
        Exemple: 2024-001
        """
        annee = timezone.now().year
        # Récupère le dernier numero de facture pour cette année
        dernier_numero = (
            Facture.objects.filter(numero__startswith=f"{annee}-")
            .order_by("-numero")
            .first()
        )

        if dernier_numero:
            # Extrait le numero et l'incrémente
            try:
                dernier_num = int(dernier_numero.numero.split("-")[1])
                nouveau_num = dernier_num + 1
            except (IndexError, ValueError):
                nouveau_num = 1
        else:
            nouveau_num = 1

        # Formate le nouveau numero avec des zéros devant
        return f"{annee}-{nouveau_num:03d}"

    def get_statut_badge_class(self):
        """
        Retourne la classe CSS du badge en fonction du statut
        """
        statut_classes = {
            "envoyée": "bg-primary",
            "payée": "bg-success",
            "en_retard": "bg-danger",
            "annulée": "bg-secondary",
            "brouillon": "bg-warning",
        }
        return statut_classes.get(self.statut_paiement, "bg-secondary")
