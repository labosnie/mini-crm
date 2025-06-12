from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from clients.models import Client, Tag


class ClientViewTest(TestCase):
    def setUp(self):
        self.test_client = TestClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.test_client.login(username="testuser", password="testpassword")

        # Crée un client de test
        self.client_obj = Client.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            telephone="0123456789",
            ville="Paris",
            statut="actif"
        )

    def test_client_list_view(self):
        """Test la vue liste des clients"""
        response = self.test_client.get(reverse("clients:client_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clients/client_list.html")
        self.assertContains(response, "Jean Dupont")

    def test_client_detail_view(self):
        """Test la vue détaillée d'un client"""
        response = self.test_client.get(
            reverse("clients:client_detail", args=[self.client_obj.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clients/client_detail.html")
        self.assertContains(response, "Jean Dupont")

    def test_client_create_view(self):
        """Test la création d'un client"""
        data = {
            "nom": "Martin",
            "prenom": "Sophie",
            "email": "sophie.martin@example.com",
            "telephone": "0987654321",
            "ville": "Lyon",
            "statut": "prospect"
        }
        response = self.test_client.post(reverse("clients:client_create"), data)
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(Client.objects.filter(email="sophie.martin@example.com").exists())

    def test_client_update_view(self):
        """Test la modification d'un client"""
        data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@example.com",
            "telephone": "0123456789",
            "ville": "Marseille",  # Changement de ville
            "statut": "actif"
        }
        response = self.test_client.post(
            reverse("clients:client_update", args=[self.client_obj.id]),
            data
        )
        self.assertEqual(response.status_code, 302)
        updated_client = Client.objects.get(id=self.client_obj.id)
        self.assertEqual(updated_client.ville, "Marseille")

    def test_client_delete_view(self):
        """Test la suppression d'un client"""
        response = self.test_client.post(
            reverse("clients:client_delete", args=[self.client_obj.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Client.objects.filter(id=self.client_obj.id).exists())

    def test_client_export_csv(self):
        """Test l'export CSV des clients"""
        response = self.test_client.get(reverse("clients:client_export", args=["csv"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "text/csv"
        )
        content = response.content.decode()
        self.assertIn("Dupont", content)
        self.assertIn("Jean", content)

    def test_client_export_pdf(self):
        """Test l'export PDF des clients"""
        response = self.test_client.get(reverse("clients:client_export", args=["pdf"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"], "application/pdf"
        ) 