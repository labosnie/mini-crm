from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse


class AuthAPITestCase(APITestCase):
    """Tests pour l'authentification API"""

    def setUp(self):
        """Configuration initiale pour tous les tests"""
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Configurer le client API
        self.client = APIClient()

    def test_obtain_token_valid_credentials(self):
        """Test d'obtention d'un token avec des identifiants valides"""
        url = reverse("api:auth_login")
        data = {"username": "testuser", "password": "testpass123"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        # Vérifier que le token existe en base
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data["token"], token.key)

    def test_obtain_token_invalid_credentials(self):
        """Test d'obtention d'un token avec des identifiants invalides"""
        url = reverse("api:auth_login")
        data = {"username": "testuser", "password": "wrongpassword"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_obtain_token_nonexistent_user(self):
        """Test d'obtention d'un token avec un utilisateur inexistant"""
        url = reverse("api:auth_login")
        data = {"username": "nonexistent", "password": "testpass123"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_obtain_token_missing_fields(self):
        """Test d'obtention d'un token avec des champs manquants"""
        url = reverse("api:auth_login")
        data = {"username": "testuser"}  # Mot de passe manquant
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_creation_on_first_login(self):
        """Test de création automatique d'un token lors de la première connexion"""
        # Créer un nouvel utilisateur
        user = User.objects.create_user(
            username="newuser", password="testpass123", email="new@test.com"
        )

        # Première connexion - devrait créer un token
        url = reverse("api:auth_login")
        data = {"username": "newuser", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_api_access_with_token(self):
        """Test d'accès à l'API avec un token valide"""
        # Obtenir un token
        url = reverse("api:auth_login")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        token = response.data["token"]

        # Tester l'accès à un endpoint protégé
        url = reverse("api:client-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_access_without_token(self):
        """Test d'accès à l'API sans token"""
        url = reverse("api:client-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_access_with_invalid_token(self):
        """Test d'accès à l'API avec un token invalide"""
        url = reverse("api:client-list")
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid_token")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
