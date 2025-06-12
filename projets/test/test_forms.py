from django.test import TestCase
from projets.forms import ProjetForm
from clients.models import Client
from django.utils import timezone


class ProjetFormTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            nom="Client de test",
            email="client@example.com"
        )

    def test_projet_form_valid(self):
        """Test un formulaire valide"""
        form_data = {
            "titre": "Projet de test",
            "description": "Description du projet de test",
            "client": self.client.id,
            "date_debut": timezone.now().date(),
            "statut": "en_cours",
            "montant": 1000.00
        }
        form = ProjetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_projet_form_invalid(self):
        """Test un formulaire invalide"""
        form_data = {
            "titre": "",  # Champ obligatoire vide
            "description": "Description du projet de test",
            "client": self.client.id,
            "date_debut": timezone.now().date(),
            "statut": "en_cours",
            "montant": -1000.00  # Montant négatif
        }
        form = ProjetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("titre", form.errors)
        self.assertIn("montant", form.errors) 