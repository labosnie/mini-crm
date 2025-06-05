from django.utils import timezone
from django.test import TestCase
from factures.forms import FactureForm, StatutFactureForm
from clients.models import Client
from projets.models import Projet

class FactureFormTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(nom="Client de test")
        self.projet = Projet.objects.create(
            titre="Projet de test",
            client=self.client,
            date_debut=timezone.now(),
        )

    def test_facture_form_valid(self):
        """Test un formulaire valide est valide"""
        form_data = {
            'numero': 'FACT-001',
            'client': self.client.id,
            'projet': self.projet.id,
            'montant': 1000.00,
            'statut_paiement': 'envoyée',
        }
        form = FactureForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_facture_form_invalid(self):
        """Test un formualaire invalide n'est pas valide"""
        form_data = {
            'numero': '',
            'client': self.client.id,
            'projet': self.projet.id,
            'montant': -1000.00, # Montant négatif
            'statut_paiement': 'envoyée',
        }
        form = FactureForm(data=form_data)
        self.assertFalse(form.is_valid())
            
        
