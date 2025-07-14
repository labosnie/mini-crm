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


class ProjetAPITestCase(APITestCase):
    """Tests pour l'API des projets"""

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
            date_fin=(datetime.now() + timedelta(days=30)).date(),
            montant=5000.00,
            statut="en_cours",
        )

        # Créer une facture de test pour le projet
        self.facture = Facture.objects.create(
            client=self.client_obj,
            projet=self.projet,
            montant=2500.00,
            date_emission=datetime.now().date(),
            date_echeance=(datetime.now() + timedelta(days=30)).date(),
            statut_paiement="envoyée",
        )

        # Configurer le client API avec authentification
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_list_projets_authenticated(self):
        """Test de récupération de la liste des projets avec authentification"""
        url = "/api/v1/projets/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)

    def test_list_projets_unauthenticated(self):
        """Test de récupération de la liste des projets sans authentification"""
        self.client.credentials()  # Supprimer l'authentification
        url = "/api/v1/projets/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_projet(self):
        """Test de création d'un nouveau projet"""
        url = "/api/v1/projets/"
        data = {
            "titre": "Nouveau Projet",
            "description": "Description du nouveau projet",
            "client": self.client_obj.id,
            "date_debut": datetime.now().strftime("%Y-%m-%d"),
            "date_fin": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
            "montant": 8000.00,
            "statut": "en_cours",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Projet.objects.count(), 2)

    def test_create_projet_invalid_data(self):
        """Test de création d'un projet avec des données invalides"""
        url = "/api/v1/projets/"
        data = {
            "titre": "",  # Titre vide invalide
            "description": "Description du projet",
            "client": self.client_obj.id,
            "date_debut": datetime.now().strftime("%Y-%m-%d"),
            "statut": "en_cours",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_projet(self):
        """Test de récupération d'un projet spécifique"""
        url = f"/api/v1/projets/{self.projet.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titre"], "Projet Test")

    def test_update_projet(self):
        """Test de mise à jour d'un projet"""
        url = f"/api/v1/projets/{self.projet.id}/"
        data = {"montant": 6000.00}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["montant"], "6000.00")

    def test_delete_projet(self):
        """Test de suppression d'un projet"""
        url = f"/api/v1/projets/{self.projet.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Projet.objects.count(), 0)

    def test_search_projets(self):
        """Test de recherche de projets"""
        url = "/api/v1/projets/?search=Test"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)

    def test_filter_projets_by_statut(self):
        """Test de filtrage des projets par statut"""
        url = "/api/v1/projets/?statut=en_cours"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for projet in response.data["results"]:
            self.assertEqual(projet["statut"], "en_cours")

    def test_update_projet_statut(self):
        """Test de mise à jour du statut d'un projet"""
        url = f"/api/v1/projets/{self.projet.id}/update_statut/"
        data = {"statut": "termine"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["statut"], "termine")

    def test_projets_en_cours(self):
        """Test de récupération des projets en cours"""
        url = "/api/v1/projets/en_cours/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("projets_en_cours", response.data)  # pour en_cours

    def test_projets_termines(self):
        """Test de récupération des projets terminés"""
        url = "/api/v1/projets/termines/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("projets_termines", response.data)  # pour termines

    def test_projet_factures(self):
        """Test de récupération des factures d'un projet"""
        url = f"/api/v1/projets/{self.projet.id}/factures/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_projet_stats(self):
        """Test de l'endpoint des statistiques des projets"""
        url = "/api/v1/projets/stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_projets", response.data)
        self.assertIn("montant_total", response.data)
