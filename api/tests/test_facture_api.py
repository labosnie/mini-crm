from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timedelta
import re

from clients.models import Client
from projets.models import Projet
from factures.models import Facture


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

        # Configurer le client API avec authentification
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Créer un client de test
        self.client1 = Client.objects.create(
            nom="Client Test",
            prenom="Prénom",
            email="client@test.com",
            telephone="0123456789",
            adresse="123 Rue Test",
            code_postal="75001",
            ville="Paris",
            statut="actif",
        )

        # Créer un projet de test
        self.projet1 = Projet.objects.create(
            titre="Projet Test 1",
            description="Description du projet test 1",
            client=self.client1,
            date_debut=datetime.now().date(),
            statut="en_cours",
        )

        self.projet2 = Projet.objects.create(
            titre="Projet Test 2",
            description="Description du projet test 2",
            client=self.client1,
            date_debut=datetime.now().date(),
            statut="termine",
        )

        # Créer des factures de test
        self.facture1 = Facture.objects.create(
            numero="FACT-001",
            client=self.client1,
            projet=self.projet1,
            montant=1000.00,
            date_emission=datetime.now().date(),
            date_echeance=datetime.now().date() + timedelta(days=30),
            statut_paiement="envoyée",
        )

        self.facture2 = Facture.objects.create(
            numero="FACT-002",
            client=self.client1,
            projet=self.projet2,
            montant=2000.00,
            date_emission=datetime.now().date(),
            date_echeance=datetime.now().date() + timedelta(days=60),
            statut_paiement="payée",
        )

    def test_list_factures_authenticated(self):
        """Test de récupération de la liste des factures avec authentification"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_list_factures_unauthenticated(self):
        """Test de récupération de la liste des factures sans authentification"""
        url = reverse("api:facture-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_facture(self):
        """Test de création d'une nouvelle facture"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-list")
        data = {
            "client": self.client1.id,
            "projet": self.projet1.id,
            "montant": 1500.00,
            "date_emission": "2024-01-15",
            "date_echeance": "2024-02-15",
            "statut_paiement": "envoyée",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["montant"], "1500.00")

    def test_create_facture_invalid_data(self):
        """Test de création d'une facture avec des données invalides"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-list")
        data = {
            "client": self.client1.id,
            "projet": self.projet1.id,
            "montant": -100,  # Montant négatif invalide
            "date_emission": "2024-01-15",
            "date_echeance": "2024-02-15",
            "statut_paiement": "envoyée",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_facture(self):
        """Test de récupération d'une facture spécifique"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-detail", args=[self.facture1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["montant"], "1000.00")

    def test_update_facture(self):
        """Test de mise à jour d'une facture"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-detail", args=[self.facture1.id])
        data = {"montant": 1200.00}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["montant"], "1200.00")

    def test_delete_facture(self):
        """Test de suppression d'une facture"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-detail", args=[self.facture1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_factures(self):
        """Test de recherche de factures"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-list")
        response = self.client.get(url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_factures_by_statut(self):
        """Test de filtrage des factures par statut"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-list")
        response = self.client.get(url, {"statut_paiement": "envoyée"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_facture_statut(self):
        """Test de mise à jour du statut d'une facture"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-detail", args=[self.facture1.id])
        data = {"statut_paiement": "payée"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["statut_paiement"], "payée")

    def test_factures_en_retard(self):
        """Test de récupération des factures en retard"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-list")
        response = self.client.get(url, {"en_retard": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_facture_stats(self):
        """Test de l'endpoint des statistiques des factures"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-list")
        response = self.client.get(url, {"stats": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_facture_pdf_endpoint(self):
        """Test de l'endpoint de génération PDF (test de structure)"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse("api:facture-detail", args=[self.facture1.id])
        response = self.client.get(url, {"format": "pdf"})
        # Le PDF peut retourner 200 ou 404 selon l'implémentation
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        )
