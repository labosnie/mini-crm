from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from clients.models import Client, Interaction
from projets.models import Projet
from datetime import datetime


class ClientAPITestCase(APITestCase):
    """Tests pour l'API des clients"""

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

        # Configurer le client API avec authentification
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_list_clients_authenticated(self):
        """Test de récupération de la liste des clients avec authentification"""
        url = "/api/v1/clients"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)

    def test_list_clients_unauthenticated(self):
        """Test de récupération de la liste des clients sans authentification"""
        self.client.credentials()  # Supprimer l'authentification
        url = "/api/v1/clients"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_client(self):
        """Test de création d'un nouveau client"""
        url = "/api/v1/clients"
        data = {
            "nom": "Nouveau Client",
            "email": "nouveau@test.com",
            "telephone": "0987654321",
            "adresse": "456 Rue Nouvelle",
            "code_postal": "75002",
            "ville": "Paris",
            "statut": "actif",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 2)

    def test_create_client_invalid_email(self):
        """Test de création d'un client avec un email déjà existant"""
        url = "/api/v1/clients"
        data = {
            "nom": "Client Duplicate",
            "email": "client@test.com",  # Email déjà existant
            "telephone": "1111111111",
            "adresse": "789 Rue Duplicate",
            "code_postal": "75003",
            "ville": "Paris",
            "statut": "actif",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_client(self):
        """Test de récupération d'un client spécifique"""
        url = f"/api/v1/clients/{self.client_obj.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom"], "Client Test")

    def test_update_client(self):
        """Test de mise à jour d'un client"""
        url = f"/api/v1/clients/{self.client_obj.id}"
        data = {"telephone": "9999999999"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["telephone"], "9999999999")

    def test_delete_client(self):
        """Test de suppression d'un client"""
        url = f"/api/v1/clients/{self.client_obj.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)

    def test_search_clients(self):
        """Test de recherche de clients"""
        url = "/api/v1/clients?search=Test"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["results"]), 0)

    def test_filter_clients_by_statut(self):
        """Test de filtrage des clients par statut"""
        url = "/api/v1/clients?statut=actif"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for client in response.data["results"]:
            self.assertEqual(client["statut"], "actif")

    def test_client_stats(self):
        """Test de l'endpoint des statistiques des clients"""
        url = "/api/v1/clients/stats"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_clients", response.data)
        self.assertIn("clients_actifs", response.data)

    def test_add_interaction_to_client(self):
        """Test d'ajout d'une interaction à un client"""
        url = f"/api/v1/clients/{self.client_obj.id}/add_interaction"
        data = {
            "type": "appel",
            "description": "Appel de suivi",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Interaction.objects.count(), 1)

    def test_get_client_interactions(self):
        """Test de récupération des interactions d'un client"""
        # Créer une interaction d'abord
        Interaction.objects.create(
            client=self.client_obj,
            type="appel",
            description="Test interaction",
            utilisateur=self.user,
        )

        url = f"/api/v1/clients/{self.client_obj.id}/interactions"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
