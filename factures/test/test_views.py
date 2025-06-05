from django.utils import timezone
from django.test import TestCase, Client as TestClient
from django.urls import reverse
from factures.models import Facture
from clients.models import Client
from projets.models import Projet
from django.contrib.auth.models import User

class FactureViewTest(TestCase):
    def setUp(self):
        self.test_client = TestClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.test_client.login(username="testuser", password="testpassword")

        # Crée les données de test
        self.client_obj = Client.objects.create(nom="Client de test")
        self.projet = Projet.objects.create(
            titre="Projet test",
            client=self.client_obj,
            date_debut=timezone.now(),
        )
        self.facture = Facture.objects.create(
            numero="FACT-001",
            client=self.client_obj,
            projet=self.projet,
            montant=1000.00,
            date_emission=timezone.now(),
            statut_paiement="envoyée",
        )
            
    def test_facture_list_view(self):
        """Test la vue liste des factures"""
        response = self.test_client.get(reverse('factures:facture_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/facture_list.html')
        self.assertContains(response, "FACT-001")

    def test_facture_detail_view(self):
        """Test la vue détaillée d'une facture"""
        response = self.test_client.get(
            reverse('factures:facture_detail', args=[self.facture.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/facture_detail.html')
        self.assertContains(response, "FACT-001")

    def test_facture_create_view(self):
        """Test la création d'une facture"""
        data = {
            'numero': 'FACT-002',
            'client': self.client_obj.id,
            'projet': self.projet.id,
            'montant': 2000.00,
            'statut_paiement': 'envoyée',
        }
        response = self.test_client.post(reverse('factures:facture_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(Facture.objects.filter(numero='FACT-002').exists())


    
            
 