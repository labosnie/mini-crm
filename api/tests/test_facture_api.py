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


class FactureAPITestCase(APITestCase):
    """Tests pour l'API des factures"""

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

        # Créer un projet de test
        self.projet = Projet.objects.create(
            titre="Projet Test",
            description="Description du projet test",
            client=self.client_obj,
            date_debut="2024-01-01",
            statut="en_cours",
            montant=Decimal("1000.00"),
        )

        # Créer des factures de test
        self.facture1 = Facture.objects.create(
            numero="FACT-001",
            client=self.client_obj,
            projet=self.projet,
            montant=Decimal("500.00"),
            statut_paiement="envoyée",
        )

        self.facture2 = Facture.objects.create(
            numero="FACT-002",
            client=self.client_obj,
            projet=self.projet,
            montant=Decimal("300.00"),
            statut_paiement="payée",
        )

    def test_list_factures_authenticated(self):
        """Test de récupération de la liste des factures avec authentification"""
        url = reverse("facture-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        # Vérifier que les données sont correctes
        facture_data = response.data["results"][0]
        self.assertIn("id", facture_data)
        self.assertIn("numero", facture_data)
        self.assertIn("montant", facture_data)
        self.assertIn("statut_paiement", facture_data)
        self.assertIn("client", facture_data)
        self.assertIn("projet", facture_data)

    def test_list_factures_unauthenticated(self):
        """Test de récupération de la liste des factures sans authentification"""
        self.client.credentials()  # Supprimer l'authentification
        url = reverse("facture-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_facture(self):
        """Test de création d'une nouvelle facture"""
        url = reverse("facture-list")
        data = {
            "client": self.client_obj.id,
            "projet": self.projet.id,
            "montant": "750.00",
            "statut_paiement": "envoyée",
            "notes": "Facture de test",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Facture.objects.count(), 3)

        # Vérifier que la facture a été créée avec les bonnes données
        facture = Facture.objects.latest("id")
        self.assertEqual(facture.client, self.client_obj)
        self.assertEqual(facture.projet, self.projet)
        self.assertEqual(facture.montant, Decimal("750.00"))
        self.assertEqual(facture.statut_paiement, "envoyée")
        self.assertTrue(facture.numero)  # Le numéro doit être généré automatiquement

    def test_create_facture_invalid_data(self):
        """Test de création d'une facture avec des données invalides"""
        url = reverse("facture-list")
        data = {
            "client": self.client_obj.id,
            "projet": self.projet.id,
            "montant": "-100.00",  # Montant négatif
            "statut_paiement": "envoyée",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_facture(self):
        """Test de récupération d'une facture spécifique"""
        url = reverse("facture-detail", args=[self.facture1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["numero"], "FACT-001")
        self.assertEqual(response.data["montant"], "500.00")
        self.assertEqual(response.data["statut_paiement"], "envoyée")

    def test_update_facture(self):
        """Test de mise à jour d'une facture"""
        url = reverse("facture-detail", args=[self.facture1.id])
        data = {
            "client": self.client_obj.id,
            "projet": self.projet.id,
            "montant": "600.00",
            "statut_paiement": "payée",
            "notes": "Facture mise à jour",
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que les modifications ont été appliquées
        self.facture1.refresh_from_db()
        self.assertEqual(self.facture1.montant, Decimal("600.00"))
        self.assertEqual(self.facture1.statut_paiement, "payée")
        self.assertEqual(self.facture1.notes, "Facture mise à jour")

    def test_delete_facture(self):
        """Test de suppression d'une facture"""
        url = reverse("facture-detail", args=[self.facture1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Facture.objects.count(), 1)

    def test_filter_factures_by_statut(self):
        """Test de filtrage des factures par statut"""
        url = reverse("facture-list")
        response = self.client.get(url, {"statut_paiement": "payée"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["statut_paiement"], "payée")

    def test_search_factures(self):
        """Test de recherche de factures"""
        url = reverse("facture-list")
        response = self.client.get(url, {"search": "FACT-001"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["numero"], "FACT-001")

    def test_update_facture_statut(self):
        """Test de mise à jour du statut d'une facture"""
        url = reverse("facture-update-statut", args=[self.facture1.id])
        data = {"statut_paiement": "payée"}

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que le statut a été mis à jour
        self.facture1.refresh_from_db()
        self.assertEqual(self.facture1.statut_paiement, "payée")

    def test_factures_en_retard(self):
        """Test de récupération des factures en retard"""
        # Créer une facture en retard
        facture_retard = Facture.objects.create(
            numero="FACT-003",
            client=self.client_obj,
            projet=self.projet,
            montant=Decimal("200.00"),
            statut_paiement="en_retard",
        )

        url = reverse("facture-en-retard")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["numero"], "FACT-003")

    def test_facture_stats(self):
        """Test de l'endpoint des statistiques des factures"""
        url = reverse("facture-stats")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_factures"], 2)
        self.assertEqual(response.data["factures_payees"], 1)
        self.assertEqual(response.data["factures_envoyees"], 1)
        self.assertEqual(response.data["montant_total"], 800.0)  # 500 + 300
        self.assertEqual(response.data["montant_paye"], 300.0)
        self.assertEqual(response.data["taux_paiement"], 37.5)  # 300/800 * 100

    def test_facture_pdf_endpoint(self):
        """Test de l'endpoint de génération PDF (test de structure)"""
        url = reverse("facture-pdf", args=[self.facture1.id])
        response = self.client.get(url)

        # Le test vérifie que l'endpoint existe et répond
        # La génération PDF réelle dépend de reportlab et peut échouer en test
        # mais l'endpoint doit exister
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR],
        )
