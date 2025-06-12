from django.test import TestCase
from django.utils import timezone
from projets.models import Projet
from clients.models import Client


class ProjetModelTest(TestCase):
    def setUp(self):
        # Crée un client de test
        self.client = Client.objects.create(
            nom="Client de test",
            email="client@example.com"
        )

        # Crée un projet de test
        self.projet = Projet.objects.create(
            titre="Projet de test",
            description="Description du projet de test",
            client=self.client,
            date_debut=timezone.now().date(),
            statut="en_cours",
            montant=1000.00
        )

    def test_projet_creation(self):
        """Test la création d'un projet"""
        self.assertEqual(self.projet.titre, "Projet de test")
        self.assertEqual(self.projet.description, "Description du projet de test")
        self.assertEqual(self.projet.client, self.client)
        self.assertEqual(self.projet.statut, "en_cours")
        self.assertEqual(self.projet.montant, 1000.00)

    def test_projet_str_method(self):
        """Test la méthode __str__ du projet"""
        expected_str = "Projet de test"
        self.assertEqual(str(self.projet), expected_str) 