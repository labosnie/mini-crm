from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timedelta

from clients.models import Client
from projets.models import Projet
from factures.models import Facture


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

        # Créer des projets de test
        self.projet1 = Projet.objects.create(
            titre="Projet Test 1",
            description="Description du projet test 1",
            client=self.client1,
            date_debut=datetime.now().date(),
            date_fin=datetime.now().date() + timedelta(days=30),
            statut="en_cours",
            montant=5000.00,
        )

        self.projet2 = Projet.objects.create(
            titre="Projet Test 2",
            description="Description du projet test 2",
            client=self.client1,
            date_debut=datetime.now().date() - timedelta(days=60),
            date_fin=datetime.now().date() - timedelta(days=30),
            statut="termine",
            montant=3000.00,
        )

        # Créer des factures de test
        self.facture1 = Facture.objects.create(
            numero="FACT-001",
            client=self.client1,
            projet=self.projet1,
            montant=2000.00,
            date_emission=datetime.now().date(),
            statut_paiement="envoyée",
        )

        self.facture2 = Facture.objects.create(
            numero="FACT-002",
            client=self.client1,
            projet=self.projet1,
            montant=3000.00,
            date_emission=datetime.now().date(),
            statut_paiement="payée",
        )

    def test_list_projets_authenticated(self):
        """Test de récupération de la liste des projets avec authentification"""
        url = reverse("api:projet-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        # Vérifier que les données sont correctes
        projet_data = response.data["results"][0]
        self.assertIn("id", projet_data)
        self.assertIn("titre", projet_data)
        self.assertIn("description", projet_data)
        self.assertIn("statut", projet_data)
        self.assertIn("client", projet_data)
        self.assertIn("factures_count", projet_data)
        self.assertIn("montant_total_factures", projet_data)

    def test_list_projets_unauthenticated(self):
        """Test de récupération de la liste des projets sans authentification"""
        self.client.credentials()  # Supprimer l'authentification
        url = reverse("api:projet-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_projet(self):
        """Test de création d'un nouveau projet"""
        url = reverse("api:projet-list")
        data = {
            "titre": "Nouveau Projet",
            "description": "Description du nouveau projet",
            "client": self.client1.id,
            "date_debut": datetime.now().date().isoformat(),
            "date_fin": (datetime.now().date() + timedelta(days=90)).isoformat(),
            "statut": "en_cours",
            "montant": 8000.00,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Projet.objects.count(), 3)
        self.assertEqual(response.data["titre"], "Nouveau Projet")

    def test_create_projet_invalid_data(self):
        """Test de création d'un projet avec des données invalides"""
        url = reverse("api:projet-list")
        data = {
            "titre": "",  # Titre vide
            "description": "Description du projet",
            "client": self.client1.id,
            "date_debut": datetime.now().date().isoformat(),
            "statut": "en_cours",
            "montant": -1000,  # Montant négatif
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_projet(self):
        """Test de récupération d'un projet spécifique"""
        url = reverse("api:projet-detail", args=[self.projet1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titre"], "Projet Test 1")
        self.assertEqual(response.data["montant"], "5000.00")

    def test_update_projet(self):
        """Test de mise à jour d'un projet"""
        url = reverse("api:projet-detail", args=[self.projet1.id])
        data = {
            "titre": "Projet Modifié",
            "description": "Description modifiée",
            "client": self.client1.id,
            "date_debut": datetime.now().date().isoformat(),
            "date_fin": (datetime.now().date() + timedelta(days=45)).isoformat(),
            "statut": "en_cours",
            "montant": 6000.00,
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titre"], "Projet Modifié")
        self.assertEqual(response.data["montant"], "6000.00")

        # Vérifier en base
        self.projet1.refresh_from_db()
        self.assertEqual(self.projet1.titre, "Projet Modifié")

    def test_delete_projet(self):
        """Test de suppression d'un projet"""
        url = reverse("api:projet-detail", args=[self.projet1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Projet.objects.count(), 1)

    def test_filter_projets_by_statut(self):
        """Test de filtrage des projets par statut"""
        url = reverse("api:projet-list")
        response = self.client.get(url, {"statut": "en_cours"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["statut"], "en_cours")

    def test_search_projets(self):
        """Test de recherche de projets"""
        url = reverse("api:projet-list")
        response = self.client.get(url, {"search": "Test 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["titre"], "Projet Test 1")

    def test_update_projet_statut(self):
        """Test de mise à jour du statut d'un projet"""
        url = reverse("api:projet-update-statut", args=[self.projet1.id])
        data = {"statut": "termine"}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["statut"], "termine")

        # Vérifier en base
        self.projet1.refresh_from_db()
        self.assertEqual(self.projet1.statut, "termine")

    def test_projets_en_cours(self):
        """Test de récupération des projets en cours"""
        url = reverse("api:projet-en-cours")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("projets_en_cours", response.data)

    def test_projets_termines(self):
        """Test de récupération des projets terminés"""
        url = reverse("api:projet-termines")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("projets_termines", response.data)

    def test_projet_factures(self):
        """Test de récupération des factures d'un projet"""
        url = reverse("api:projet-factures", args=[self.projet1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Vérifier que les factures sont bien celles du projet
        facture_numeros = [f["numero"] for f in response.data]
        self.assertIn("FACT-001", facture_numeros)
        self.assertIn("FACT-002", facture_numeros)

    def test_projet_stats(self):
        """Test de l'endpoint des statistiques des projets"""
        url = reverse("api:projet-stats")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_projets", response.data)
        self.assertIn("projets_en_cours", response.data)
        self.assertIn("projets_termines", response.data)
        self.assertIn("montant_total", response.data)
