from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from clients.models import Client
from projets.models import Projet
from factures.models import Facture
from datetime import datetime, timedelta


class FactureAPITestCase(APITestCase):
    """Tests pour l'API des factures"""

    def setUp(self):
        """Configuration initiale pour tous les tests"""
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Créer un token pour l'utilisateur
        self.token = Token.objects.create(user=self.user)

        # Créer un client de test
        self.client_obj = Client.objects.create(
            nom="Client Test",
            email="client@test.com",
            telephone="0123456789",
            adresse="123 Rue Test",
            code_postal="75001",
            ville="Paris",
            statut="actif",
        )

        # Créer un projet de test
        self.projet = Projet.objects.create(
            titre="Projet Test",
            description="Description du projet test",
            client=self.client_obj,
            date_debut=datetime.now().date(),
            statut="en_cours",
        )

        # Créer une facture de test
        self.facture = Facture.objects.create(
            client=self.client_obj,
            projet=self.projet,
            montant=1000.00,
            date_emission=datetime.now().date(),
            date_echeance=(datetime.now() + timedelta(days=30)).date(),
            statut_paiement="envoyée",
        )

        # Configurer le client API avec authentification
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_list_factures_authenticated(self):
        """Test de récupération de la liste des factures avec authentification"""
        url = "/api/v1/factures/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)

    def test_list_factures_unauthenticated(self):
        """Test de récupération de la liste des factures sans authentification"""
        self.client.credentials()  # Supprimer l'authentification
        url = "/api/v1/factures/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_facture(self):
        """Test de création d'une nouvelle facture"""
        url = "/api/v1/factures/"
        data = {
            "client": self.client_obj.id,
            "projet": self.projet.id,
            "montant": 2000.00,
            "date_emission": datetime.now().strftime("%Y-%m-%d"),
            "date_echeance": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "statut_paiement": "envoyée",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Facture.objects.count(), 2)

    def test_create_facture_invalid_data(self):
        """Test de création d'une facture avec des données invalides"""
        url = "/api/v1/factures/"
        data = {
            "client": self.client_obj.id,
            "projet": self.projet.id,
            "montant": -100,  # Montant négatif invalide
            "date_emission": datetime.now().strftime("%Y-%m-%d"),
            "statut_paiement": "envoyée",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_facture(self):
        """Test de récupération d'une facture spécifique"""
        url = f"/api/v1/factures/{self.facture.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["montant"], "1000.00")

    def test_update_facture(self):
        """Test de mise à jour d'une facture"""
        url = f"/api/v1/factures/{self.facture.id}/"
        data = {"montant": 1500.00}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["montant"], "1500.00")

    def test_delete_facture(self):
        """Test de suppression d'une facture"""
        url = f"/api/v1/factures/{self.facture.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Facture.objects.count(), 0)

    def test_search_factures(self):
        """Test de recherche de factures"""
        url = "/api/v1/factures/?search=Test"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)

    def test_filter_factures_by_statut(self):
        """Test de filtrage des factures par statut"""
        url = "/api/v1/factures/?statut_paiement=envoyée"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for facture in response.data["results"]:
            self.assertEqual(facture["statut_paiement"], "envoyée")

    def test_factures_en_retard(self):
        """Test de récupération des factures en retard"""
        url = "/api/v1/factures/en_retard/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("factures_en_retard", response.data)

    def test_update_facture_statut(self):
        """Test de mise à jour du statut d'une facture"""
        url = f"/api/v1/factures/{self.facture.id}/update_statut/"
        data = {"statut_paiement": "payée"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["statut_paiement"], "payée")

    def test_facture_stats(self):
        """Test de l'endpoint des statistiques des factures"""
        url = "/api/v1/factures/stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_factures", response.data)
        self.assertIn("montant_total", response.data)

    def test_facture_pdf_endpoint(self):
        """Test de l'endpoint de génération PDF (test de structure)"""
        url = f"/api/v1/factures/{self.facture.id}/pdf/"
        response = self.client.get(url)
        # Le endpoint peut retourner 200 (PDF généré) ou 404 (pas de template)
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        )
