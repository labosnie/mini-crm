from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from decimal import Decimal

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

        # Créer un token d'authentification
        self.token = Token.objects.create(user=self.user)

        # Configurer le client API avec authentification
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Créer un client de test
        self.client_obj = Client.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            telephone="0123456789",
            statut="actif",
        )

        # Créer des projets de test
        self.projet1 = Projet.objects.create(
            titre="Projet Web",
            description="Développement d'un site web",
            client=self.client_obj,
            date_debut="2024-01-01",
            date_fin="2024-06-30",
            statut="en_cours",
            montant=Decimal("5000.00"),
        )

        self.projet2 = Projet.objects.create(
            titre="Projet Mobile",
            description="Développement d'une application mobile",
            client=self.client_obj,
            date_debut="2024-02-01",
            statut="en_attente",
            montant=Decimal("3000.00"),
        )

        # Créer des factures pour le projet1
        self.facture1 = Facture.objects.create(
            numero="FACT-001",
            client=self.client_obj,
            projet=self.projet1,
            montant=Decimal("2000.00"),
            statut_paiement="payée",
        )

        self.facture2 = Facture.objects.create(
            numero="FACT-002",
            client=self.client_obj,
            projet=self.projet1,
            montant=Decimal("1500.00"),
            statut_paiement="envoyée",
        )

    def test_list_projets_authenticated(self):
        """Test de récupération de la liste des projets avec authentification"""
        url = reverse("projet-list")
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
        url = reverse("projet-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_projet(self):
        """Test de création d'un nouveau projet"""
        url = reverse("projet-list")
        data = {
            "titre": "Nouveau Projet",
            "description": "Description du nouveau projet",
            "client": self.client_obj.id,
            "date_debut": "2024-03-01",
            "statut": "en_attente",
            "montant": "4000.00",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Projet.objects.count(), 3)

        # Vérifier que le projet a été créé avec les bonnes données
        projet = Projet.objects.latest("id")
        self.assertEqual(projet.titre, "Nouveau Projet")
        self.assertEqual(projet.client, self.client_obj)
        self.assertEqual(projet.statut, "en_attente")
        self.assertEqual(projet.montant, Decimal("4000.00"))

    def test_create_projet_invalid_data(self):
        """Test de création d'un projet avec des données invalides"""
        url = reverse("projet-list")
        data = {
            "titre": "Projet Test",
            "description": "Description",
            "client": self.client_obj.id,
            "date_debut": "2024-01-01",
            "date_fin": "2023-12-31",  # Date de fin avant date de début
            "statut": "en_attente",
            "montant": "-1000.00",  # Montant négatif
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_projet(self):
        """Test de récupération d'un projet spécifique"""
        url = reverse("projet-detail", args=[self.projet1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titre"], "Projet Web")
        self.assertEqual(response.data["statut"], "en_cours")
        self.assertEqual(response.data["factures_count"], 2)
        self.assertEqual(response.data["montant_total_factures"], 3500.0)  # 2000 + 1500

    def test_update_projet(self):
        """Test de mise à jour d'un projet"""
        url = reverse("projet-detail", args=[self.projet1.id])
        data = {
            "titre": "Projet Web Mise à Jour",
            "description": "Description mise à jour",
            "client": self.client_obj.id,
            "date_debut": "2024-01-01",
            "date_fin": "2024-07-31",
            "statut": "termine",
            "montant": "6000.00",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que les modifications ont été appliquées
        self.projet1.refresh_from_db()
        self.assertEqual(self.projet1.titre, "Projet Web Mise à Jour")
        self.assertEqual(self.projet1.statut, "termine")
        self.assertEqual(self.projet1.montant, Decimal("6000.00"))

    def test_delete_projet(self):
        """Test de suppression d'un projet"""
        url = reverse("projet-detail", args=[self.projet1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Projet.objects.count(), 1)

    def test_filter_projets_by_statut(self):
        """Test de filtrage des projets par statut"""
        url = reverse("projet-list")
        response = self.client.get(url, {"statut": "en_cours"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["statut"], "en_cours")

    def test_search_projets(self):
        """Test de recherche de projets"""
        url = reverse("projet-list")
        response = self.client.get(url, {"search": "Web"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["titre"], "Projet Web")

    def test_update_projet_statut(self):
        """Test de mise à jour du statut d'un projet"""
        url = reverse("projet-update-statut", args=[self.projet1.id])
        data = {"statut": "termine"}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que le statut a été mis à jour
        self.projet1.refresh_from_db()
        self.assertEqual(self.projet1.statut, "termine")

    def test_projets_en_cours(self):
        """Test de récupération des projets en cours"""
        url = reverse("projet-en-cours")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["titre"], "Projet Web")

    def test_projets_termines(self):
        """Test de récupération des projets terminés"""
        # Créer un projet terminé
        projet_termine = Projet.objects.create(
            titre="Projet Terminé",
            description="Projet déjà terminé",
            client=self.client_obj,
            date_debut="2023-01-01",
            date_fin="2023-12-31",
            statut="termine",
            montant=Decimal("1000.00"),
        )

        url = reverse("projet-termines")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["titre"], "Projet Terminé")

    def test_projet_factures(self):
        """Test de récupération des factures d'un projet"""
        url = reverse("projet-factures", args=[self.projet1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Vérifier que les factures sont bien celles du projet
        facture_numeros = [f["numero"] for f in response.data]
        self.assertIn("FACT-001", facture_numeros)
        self.assertIn("FACT-002", facture_numeros)

    def test_projet_stats(self):
        """Test de l'endpoint des statistiques des projets"""
        url = reverse("projet-stats")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_projets"], 2)
        self.assertEqual(response.data["projets_en_cours"], 1)
        self.assertEqual(response.data["projets_en_attente"], 1)
        self.assertEqual(response.data["projets_termines"], 0)
        self.assertEqual(response.data["montant_total"], 8000.0)  # 5000 + 3000
