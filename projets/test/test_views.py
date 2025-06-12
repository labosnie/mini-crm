from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from projets.models import Projet
from clients.models import Client
from django.utils import timezone


class ProjetViewTest(TestCase):
    def setUp(self):
        self.test_client = TestClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.test_client.login(username="testuser", password="testpassword")

        # Crée un client de test
        self.client_obj = Client.objects.create(
            nom="Client de test", email="client@example.com"
        )

        # Crée un projet de test
        self.projet = Projet.objects.create(
            titre="Projet de test",
            description="Description du projet de test",
            client=self.client_obj,
            date_debut=timezone.now().date(),
            statut="en_cours",
            montant=1000.00,
        )

    def test_projet_list_view(self):
        """Test la vue liste des projets"""
        response = self.test_client.get(reverse("projets:projet_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projets/projet_list.html")
        self.assertContains(response, "Projet de test")

    def test_projet_detail_view(self):
        """Test la vue détaillée d'un projet"""
        response = self.test_client.get(
            reverse("projets:projet_detail", args=[self.projet.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projets/projet_detail.html")
        self.assertContains(response, "Projet de test")

    def test_projet_create_view(self):
        """Test la création d'un projet"""
        data = {
            "titre": "Nouveau projet",
            "description": "Description du nouveau projet",
            "client": self.client_obj.id,
            "date_debut": timezone.now().date(),
            "statut": "en_cours",
            "montant": 2000.00,
        }
        response = self.test_client.post(reverse("projets:projet_create"), data)
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(Projet.objects.filter(titre="Nouveau projet").exists())

    def test_projet_update_view(self):
        """Test la modification d'un projet"""
        data = {
            "titre": "Projet de test",
            "description": "Description modifiée",
            "client": self.client_obj.id,
            "date_debut": timezone.now().date(),
            "statut": "en_cours",
            "montant": 1500.00,
        }
        response = self.test_client.post(
            reverse("projets:projet_update", args=[self.projet.id]), data
        )
        self.assertEqual(response.status_code, 302)
        updated_projet = Projet.objects.get(id=self.projet.id)
        self.assertEqual(updated_projet.description, "Description modifiée")

    def test_projet_delete_view(self):
        """Test la suppression d'un projet"""
        response = self.test_client.post(
            reverse("projets:projet_delete", args=[self.projet.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Projet.objects.filter(id=self.projet.id).exists())
