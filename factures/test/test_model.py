from django.test import TestCase
from django.utils import timezone
from factures.models import Facture
from clients.models import Client
from projets.models import Projet


class FactureModelTest(TestCase):
    def setUp(self):
        # Crée un client de test
        self.client = Client.objects.create(
            nom="Client de test",
            email="client@example.com",
        )

        # Crée un projet de test
        self.projet = Projet.objects.create(
            titre="Projet de test",
            client=self.client,
            date_debut=timezone.now(),
        )

        # Crée une facture de test
        self.facture = Facture.objects.create(
            numero="FACT-001",
            client=self.client,
            projet=self.projet,
            montant=1000.00,
            date_emission=timezone.now(),
            statut_paiement="envoyée",
        )

    def test_facture_creation(self):
        """Test la crétation d'une facture"""
        self.assertEqual(self.facture.numero, "FACT-001")
        self.assertEqual(self.facture.montant, 1000.00)
        self.assertEqual(self.facture.statut_paiement, "envoyée")

    def test_facture_str_method(self):
        """Test la méthode __str__ de la facture"""
        expected_str = (
            f"Facture {self.facture.numero} - {self.client.nom} - {self.projet.titre}"
        )
        self.assertEqual(str(self.facture), expected_str)
