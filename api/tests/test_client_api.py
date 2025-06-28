from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

from clients.models import Client, Tag, Interaction


class ClientAPITestCase(APITestCase):
    """Tests pour l'API des clients"""
    
    def setUp(self):
        """Configuration initiale pour tous les tests"""
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Créer un token d'authentification
        self.token = Token.objects.create(user=self.user)
        
        # Configurer le client API avec authentification
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Créer des tags de test
        self.tag1 = Tag.objects.create(nom='VIP', couleur='#FF0000')
        self.tag2 = Tag.objects.create(nom='Prospect', couleur='#00FF00')
        
        # Créer des clients de test
        self.client1 = Client.objects.create(
            nom='Dupont',
            prenom='Jean',
            email='jean.dupont@example.com',
            telephone='0123456789',
            statut='actif'
        )
        self.client1.tags.add(self.tag1)
        
        self.client2 = Client.objects.create(
            nom='Martin',
            prenom='Marie',
            email='marie.martin@example.com',
            telephone='0987654321',
            statut='prospect'
        )
        self.client2.tags.add(self.tag2)
    
    def test_list_clients_authenticated(self):
        """Test de récupération de la liste des clients avec authentification"""
        url = reverse('client-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Vérifier que les données sont correctes
        client_data = response.data['results'][0]
        self.assertIn('id', client_data)
        self.assertIn('nom', client_data)
        self.assertIn('email', client_data)
        self.assertIn('statut', client_data)
    
    def test_list_clients_unauthenticated(self):
        """Test de récupération de la liste des clients sans authentification"""
        self.client.credentials()  # Supprimer l'authentification
        url = reverse('client-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_client(self):
        """Test de création d'un nouveau client"""
        url = reverse('client-list')
        data = {
            'nom': 'Nouveau',
            'prenom': 'Client',
            'email': 'nouveau.client@example.com',
            'telephone': '0555666777',
            'statut': 'prospect',
            'tags': [self.tag1.id]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 3)
        
        # Vérifier que le client a été créé avec les bonnes données
        client = Client.objects.get(email='nouveau.client@example.com')
        self.assertEqual(client.nom, 'Nouveau')
        self.assertEqual(client.statut, 'prospect')
        self.assertIn(self.tag1, client.tags.all())
    
    def test_create_client_invalid_email(self):
        """Test de création d'un client avec un email déjà existant"""
        url = reverse('client-list')
        data = {
            'nom': 'Test',
            'prenom': 'Client',
            'email': 'jean.dupont@example.com',  # Email déjà existant
            'statut': 'prospect'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_retrieve_client(self):
        """Test de récupération d'un client spécifique"""
        url = reverse('client-detail', args=[self.client1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nom'], 'Dupont')
        self.assertEqual(response.data['email'], 'jean.dupont@example.com')
        self.assertEqual(len(response.data['interactions']), 0)
    
    def test_update_client(self):
        """Test de mise à jour d'un client"""
        url = reverse('client-detail', args=[self.client1.id])
        data = {
            'nom': 'Dupont',
            'prenom': 'Jean-Pierre',
            'email': 'jean-pierre.dupont@example.com',  # Email différent pour éviter le conflit
            'statut': 'inactif',
            'tags': [self.tag2.id]
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que les modifications ont été appliquées
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.prenom, 'Jean-Pierre')
        self.assertEqual(self.client1.statut, 'inactif')
        self.assertIn(self.tag2, self.client1.tags.all())
    
    def test_delete_client(self):
        """Test de suppression d'un client"""
        url = reverse('client-detail', args=[self.client1.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 1)
    
    def test_filter_clients_by_statut(self):
        """Test de filtrage des clients par statut"""
        url = reverse('client-list')
        response = self.client.get(url, {'statut': 'actif'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['statut'], 'actif')
    
    def test_search_clients(self):
        """Test de recherche de clients"""
        url = reverse('client-list')
        response = self.client.get(url, {'search': 'Dupont'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nom'], 'Dupont')
    
    def test_client_stats(self):
        """Test de l'endpoint des statistiques des clients"""
        url = reverse('client-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_clients'], 2)
        self.assertEqual(response.data['clients_actifs'], 1)
        self.assertEqual(response.data['clients_prospects'], 1)
        self.assertEqual(response.data['clients_inactifs'], 0)
    
    def test_add_interaction_to_client(self):
        """Test d'ajout d'une interaction à un client"""
        url = reverse('client-add-interaction', args=[self.client1.id])
        data = {
            'type': 'appel',
            'description': 'Appel de suivi client'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Interaction.objects.count(), 1)
        
        interaction = Interaction.objects.first()
        self.assertEqual(interaction.client, self.client1)
        self.assertEqual(interaction.type, 'appel')
        self.assertEqual(interaction.utilisateur, self.user)
    
    def test_get_client_interactions(self):
        """Test de récupération des interactions d'un client"""
        # Créer une interaction
        Interaction.objects.create(
            client=self.client1,
            type='email',
            description='Email de contact',
            utilisateur=self.user
        )
        
        url = reverse('client-interactions', args=[self.client1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type'], 'email')
        self.assertEqual(response.data[0]['description'], 'Email de contact') 