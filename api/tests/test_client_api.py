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

        # Configurer le client API avec authentification
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Créer des clients de test
        self.client1 = Client.objects.create(
            nom="Client Test 1",
            prenom="Prénom",
            email="client1@test.com",
            telephone="0123456789",
            adresse="123 Rue Test",
            code_postal="75001",
            ville="Paris",
            statut="actif",
        )

        self.client2 = Client.objects.create(
            nom="Client Test 2",
            prenom="Prénom",
            email="client2@test.com",
            telephone="0987654321",
            adresse="456 Rue Test",
            code_postal="75002",
            ville="Paris",
            statut="inactif",
        )

        # Créer un projet de test
        self.projet = Projet.objects.create(
            titre="Projet Test",
            description="Description du projet test",
            client=self.client1,
            date_debut=datetime.now().date(),
            statut="en_cours",
        )

    def test_list_clients_authenticated(self):
        """Test de récupération de la liste des clients avec authentification"""
        url = reverse("api:client-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_list_clients_unauthenticated(self):
        """Test de récupération de la liste des clients sans authentification"""
        # Supprimer l'authentification
        self.client.credentials()

        url = reverse("api:client-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_client(self):
        """Test de création d'un nouveau client"""
        url = reverse("api:client-list")
        data = {
            "nom": "Nouveau Client",
            "prenom": "Prénom",
            "email": "nouveau@test.com",
            "telephone": "0123456789",
            "adresse": "789 Rue Test",
            "code_postal": "75003",
            "ville": "Paris",
            "statut": "actif",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 3)
        self.assertEqual(response.data["nom"], "Nouveau Client")

    def test_create_client_invalid_email(self):
        """Test de création d'un client avec un email déjà existant"""
        url = reverse("api:client-list")
        data = {
            "nom": "Client Dupliqué",
            "prenom": "Prénom",
            "email": "client1@test.com",  # Email déjà existant
            "telephone": "0123456789",
            "adresse": "789 Rue Test",
            "code_postal": "75003",
            "ville": "Paris",
            "statut": "actif",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_retrieve_client(self):
        """Test de récupération d'un client spécifique"""
        url = reverse("api:client-detail", args=[self.client1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom"], "Client Test 1")
        self.assertEqual(response.data["email"], "client1@test.com")

    def test_update_client(self):
        """Test de mise à jour d'un client"""
        url = reverse("api:client-detail", args=[self.client1.id])
        data = {
            "nom": "Client Modifié",
            "prenom": "Prénom",
            "email": "client1.modifie@test.com",  # Email différent pour éviter le conflit
            "telephone": "0123456789",
            "adresse": "123 Rue Test",
            "code_postal": "75001",
            "ville": "Paris",
            "statut": "actif",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nom"], "Client Modifié")

        # Vérifier en base
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.nom, "Client Modifié")

    def test_delete_client(self):
        """Test de suppression d'un client"""
        url = reverse("api:client-detail", args=[self.client1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 1)

    def test_search_clients(self):
        """Test de recherche de clients"""
        url = reverse("api:client-list")
        response = self.client.get(url, {"search": "Test 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["nom"], "Client Test 1")

    def test_filter_clients_by_statut(self):
        """Test de filtrage des clients par statut"""
        url = reverse("api:client-list")
        response = self.client.get(url, {"statut": "actif"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["statut"], "actif")

    def test_client_stats(self):
        """Test de l'endpoint des statistiques des clients"""
        url = reverse("api:client-stats")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_clients", response.data)
        self.assertIn("clients_actifs", response.data)
        self.assertIn("clients_inactifs", response.data)

    def test_add_interaction_to_client(self):
        """Test d'ajout d'une interaction à un client"""
        url = reverse("api:client-add-interaction", args=[self.client1.id])
        data = {
            "type": "appel",
            "description": "Appel de suivi",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Interaction.objects.count(), 1)
        self.assertEqual(response.data["type"], "appel")

    def test_get_client_interactions(self):
        """Test de récupération des interactions d'un client"""
        # Créer une interaction
        Interaction.objects.create(
            client=self.client1,
            type="appel",
            description="Appel de suivi",
            utilisateur=self.user,
        )

        url = reverse("api:client-interactions", args=[self.client1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["type"], "appel")
