#!/usr/bin/env python3
"""
Script de test pour l'API REST du mini-CRM
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def print_response(response, title):
    """Affiche la réponse de manière formatée"""
    print(f"\n{'='*50}")
    print(f"📋 {title}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_authentication():
    """Test de l'authentification"""
    print("\n🔐 TEST D'AUTHENTIFICATION")

    # 1. Test d'inscription
    register_data = {
        "username": "test_user",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123",
    }

    response = requests.post(
        f"{BASE_URL}/auth/register/", json=register_data, headers=HEADERS
    )
    print_response(response, "Inscription d'un nouvel utilisateur")

    # 2. Test de connexion
    login_data = {"username": "test_user", "password": "testpass123"}

    response = requests.post(
        f"{BASE_URL}/auth/login/", json=login_data, headers=HEADERS
    )
    print_response(response, "Connexion utilisateur")

    if response.status_code == 200:
        token = response.json().get("token")
        return token
    return None


def test_clients(token):
    """Test des endpoints clients"""
    print("\n👥 TEST DES CLIENTS")

    headers = {**HEADERS, "Authorization": f"Token {token}"}

    # 1. Créer un client
    client_data = {
        "nom": "Entreprise Test",
        "email": "contact@test.com",
        "telephone": "0123456789",
        "adresse": "123 Rue Test",
        "code_postal": "75001",
        "ville": "Paris",
        "statut": "actif",
    }

    response = requests.post(f"{BASE_URL}/clients/", json=client_data, headers=headers)
    print_response(response, "Création d'un client")

    if response.status_code == 201:
        client_id = response.json().get("id")

        # 2. Récupérer la liste des clients
        response = requests.get(f"{BASE_URL}/clients/", headers=headers)
        print_response(response, "Liste des clients")

        # 3. Récupérer un client spécifique
        response = requests.get(f"{BASE_URL}/clients/{client_id}/", headers=headers)
        print_response(response, f"Détails du client {client_id}")

        # 4. Mettre à jour un client
        update_data = {"telephone": "0987654321"}
        response = requests.patch(
            f"{BASE_URL}/clients/{client_id}/", json=update_data, headers=headers
        )
        print_response(response, f"Mise à jour du client {client_id}")

        return client_id
    return None


def test_projets(token, client_id):
    """Test des endpoints projets"""
    print("\n📋 TEST DES PROJETS")

    headers = {**HEADERS, "Authorization": f"Token {token}"}

    # 1. Créer un projet
    projet_data = {
        "titre": "Projet Test API",
        "description": "Projet de test pour l'API REST",
        "client": client_id,
        "date_debut": datetime.now().strftime("%Y-%m-%d"),
        "date_fin": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "montant": 5000.00,
        "statut": "en_cours",
    }

    response = requests.post(f"{BASE_URL}/projets/", json=projet_data, headers=headers)
    print_response(response, "Création d'un projet")

    if response.status_code == 201:
        projet_id = response.json().get("id")

        # 2. Récupérer la liste des projets
        response = requests.get(f"{BASE_URL}/projets/", headers=headers)
        print_response(response, "Liste des projets")

        # 3. Récupérer un projet spécifique
        response = requests.get(f"{BASE_URL}/projets/{projet_id}/", headers=headers)
        print_response(response, f"Détails du projet {projet_id}")

        # 4. Test des actions personnalisées
        response = requests.get(f"{BASE_URL}/projets/en_cours/", headers=headers)
        print_response(response, "Projets en cours")

        response = requests.get(f"{BASE_URL}/projets/stats/", headers=headers)
        print_response(response, "Statistiques des projets")

        return projet_id
    return None


def test_factures(token, client_id, projet_id):
    """Test des endpoints factures"""
    print("\n💰 TEST DES FACTURES")

    headers = {**HEADERS, "Authorization": f"Token {token}"}

    # 1. Créer une facture
    facture_data = {
        "client": client_id,
        "projet": projet_id,
        "montant": 2500.00,
        "date_emission": datetime.now().strftime("%Y-%m-%d"),
        "date_echeance": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "statut_paiement": "envoyée",
    }

    response = requests.post(
        f"{BASE_URL}/factures/", json=facture_data, headers=headers
    )
    print_response(response, "Création d'une facture")

    if response.status_code == 201:
        facture_id = response.json().get("id")

        # 2. Récupérer la liste des factures
        response = requests.get(f"{BASE_URL}/factures/", headers=headers)
        print_response(response, "Liste des factures")

        # 3. Récupérer une facture spécifique
        response = requests.get(f"{BASE_URL}/factures/{facture_id}/", headers=headers)
        print_response(response, f"Détails de la facture {facture_id}")

        # 4. Test des actions personnalisées
        response = requests.get(f"{BASE_URL}/factures/en_retard/", headers=headers)
        print_response(response, "Factures en retard")

        response = requests.get(f"{BASE_URL}/factures/stats/", headers=headers)
        print_response(response, "Statistiques des factures")

        # 5. Mettre à jour le statut d'une facture
        update_data = {"statut_paiement": "payée"}
        response = requests.patch(
            f"{BASE_URL}/factures/{facture_id}/update_statut/",
            json=update_data,
            headers=headers,
        )
        print_response(response, f"Mise à jour du statut de la facture {facture_id}")

        return facture_id
    return None


def test_filtres_et_recherche(token):
    """Test des filtres et de la recherche"""
    print("\n🔍 TEST DES FILTRES ET RECHERCHE")

    headers = {**HEADERS, "Authorization": f"Token {token}"}

    # Test de recherche dans les clients
    response = requests.get(f"{BASE_URL}/clients/?search=Test", headers=headers)
    print_response(response, "Recherche de clients contenant 'Test'")

    # Test de filtrage par statut
    response = requests.get(f"{BASE_URL}/clients/?statut=actif", headers=headers)
    print_response(response, "Clients avec statut 'actif'")

    # Test de recherche dans les factures
    response = requests.get(f"{BASE_URL}/factures/?search=Test", headers=headers)
    print_response(response, "Recherche de factures contenant 'Test'")


def test_pagination():
    """Test de la pagination"""
    print("\n📄 TEST DE LA PAGINATION")

    # Créer plusieurs clients pour tester la pagination
    token = test_authentication()
    if not token:
        return

    headers = {**HEADERS, "Authorization": f"Token {token}"}

    # Créer 5 clients supplémentaires
    for i in range(5):
        client_data = {
            "nom": f"Client Test {i+1}",
            "email": f"client{i+1}@test.com",
            "telephone": f"012345678{i}",
            "adresse": f"{i+1} Rue Test",
            "code_postal": "75001",
            "ville": "Paris",
            "statut": "actif",
        }
        requests.post(f"{BASE_URL}/clients/", json=client_data, headers=headers)

    # Test de la pagination
    response = requests.get(f"{BASE_URL}/clients/?page=1", headers=headers)
    print_response(response, "Page 1 des clients")

    response = requests.get(f"{BASE_URL}/clients/?page=2", headers=headers)
    print_response(response, "Page 2 des clients")


def main():
    """Fonction principale de test"""
    print("🚀 DÉMARRAGE DES TESTS DE L'API REST")
    print("=" * 60)

    try:
        # Test d'authentification
        token = test_authentication()
        if not token:
            print("❌ Échec de l'authentification")
            return

        # Test des clients
        client_id = test_clients(token)
        if not client_id:
            print("❌ Échec des tests clients")
            return

        # Test des projets
        projet_id = test_projets(token, client_id)
        if not projet_id:
            print("❌ Échec des tests projets")
            return

        # Test des factures
        facture_id = test_factures(token, client_id, projet_id)
        if not facture_id:
            print("❌ Échec des tests factures")
            return

        # Test des filtres et recherche
        test_filtres_et_recherche(token)

        # Test de la pagination
        test_pagination()

        print("\n✅ TOUS LES TESTS SONT TERMINÉS AVEC SUCCÈS !")
        print("\n📚 Pour plus de tests, utilisez l'interface Swagger :")
        print("   http://127.0.0.1:8000/api/v1/docs/")

    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion. Assurez-vous que le serveur Django est démarré.")
    except Exception as e:
        print(f"❌ Erreur lors des tests : {str(e)}")


if __name__ == "__main__":
    main()
