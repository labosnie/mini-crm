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
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Configurer le client API
        self.client = APIClient()
    
    def test_obtain_token_valid_credentials(self):
        """Test d'obtention d'un token avec des identifiants valides"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
        # Vérifier que le token existe en base
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)
    
    def test_obtain_token_invalid_credentials(self):
        """Test d'obtention d'un token avec des identifiants invalides"""
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_obtain_token_nonexistent_user(self):
        """Test d'obtention d'un token avec un utilisateur inexistant"""
        url = reverse('api_token_auth')
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_obtain_token_missing_fields(self):
        """Test d'obtention d'un token avec des champs manquants"""
        url = reverse('api_token_auth')
        
        # Test sans username
        data = {'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test sans password
        data = {'username': 'testuser'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_creation_on_first_login(self):
        """Test de création automatique d'un token lors de la première connexion"""
        # Supprimer le token existant s'il y en a un
        Token.objects.filter(user=self.user).delete()
        
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
        # Vérifier qu'un nouveau token a été créé
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)
    
    def test_api_access_with_token(self):
        """Test d'accès à l'API avec un token valide"""
        # Créer un token
        token = Token.objects.create(user=self.user)
        
        # Configurer le client avec le token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        # Tester l'accès à un endpoint protégé (clients)
        url = reverse('client-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_access_without_token(self):
        """Test d'accès à l'API sans token"""
        # Ne pas configurer d'authentification
        url = reverse('client-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_api_access_with_invalid_token(self):
        """Test d'accès à l'API avec un token invalide"""
        # Configurer le client avec un token invalide
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        
        url = reverse('client-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 