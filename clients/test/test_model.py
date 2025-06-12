from django.test import TestCase
from django.utils import timezone
from clients.models import Client, Interaction, Tag
from django.contrib.auth.models import User


class ClientModelTest(TestCase):
    def setUp(self):
        # Crée un client de test
        self.client = Client.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            telephone="0123456789",
            adresse="123 rue de Paris",
            ville="Paris",
            code_postal="75001",
            pays="France",
            statut="actif",
            notes="Client important",
        )

    def test_client_creation(self):
        """Test la création d'un client"""
        self.assertEqual(self.client.nom, "Dupont")
        self.assertEqual(self.client.prenom, "Jean")
        self.assertEqual(self.client.email, "jean.dupont@example.com")
        self.assertEqual(self.client.telephone, "0123456789")
        self.assertEqual(self.client.ville, "Paris")
        self.assertEqual(self.client.statut, "actif")

    def test_client_str_method(self):
        """Test la méthode __str__ du client"""
        expected_str = "Jean Dupont"
        self.assertEqual(str(self.client), expected_str)

    def test_client_without_prenom(self):
        """Test la méthode __str__ du client sans prénom"""
        client = Client.objects.create(
            nom="Martin", email="martin@example.com", statut="prospect"
        )
        self.assertEqual(str(client), "Martin")


class InteractionModelTest(TestCase):
    def setUp(self):
        # Crée un utilisateur de test
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Crée un client de test
        self.client = Client.objects.create(nom="Test", email="test@example.com")

        # Crée une interaction de test
        self.interaction = Interaction.objects.create(
            client=self.client,
            type="appel",
            description="Appel de suivi",
            utilisateur=self.user,
        )

    def test_interaction_creation(self):
        """Test la création d'une interaction"""
        self.assertEqual(self.interaction.client, self.client)
        self.assertEqual(self.interaction.type, "appel")
        self.assertEqual(self.interaction.description, "Appel de suivi")
        self.assertEqual(self.interaction.utilisateur, self.user)

    def test_interaction_ordering(self):
        """Test l'ordre des interactions"""
        interaction2 = Interaction.objects.create(
            client=self.client,
            type="email",
            description="Email de suivi",
            utilisateur=self.user,
        )
        interactions = Interaction.objects.all()
        self.assertEqual(interactions[0], interaction2)  # La plus récente en premier
