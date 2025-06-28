#!/bin/bash

# Script de test pour l'API REST avec cURL
# Usage: ./test_api_curl.sh

BASE_URL="http://127.0.0.1:8000/api/v1"

echo "🚀 DÉMARRAGE DES TESTS DE L'API REST AVEC CURL"
echo "=============================================="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_response() {
    local title="$1"
    local status="$2"
    local response="$3"
    
    echo -e "\n${BLUE}=================================================="
    echo -e "📋 $title"
    echo -e "==================================================${NC}"
    echo -e "Status: $status"
    echo -e "Response: $response"
}

# Test 1: Inscription d'un utilisateur
echo -e "\n${YELLOW}🔐 TEST D'INSCRIPTION${NC}"
REGISTER_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/register/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "test_user_curl",
        "email": "test_curl@example.com",
        "first_name": "Test",
        "last_name": "Curl",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }')

HTTP_STATUS=$(echo "$REGISTER_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$REGISTER_RESPONSE" | head -n -1)
print_response "Inscription utilisateur" "$HTTP_STATUS" "$RESPONSE_BODY"

# Test 2: Connexion et récupération du token
echo -e "\n${YELLOW}🔑 TEST DE CONNEXION${NC}"
LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/login/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "test_user_curl",
        "password": "testpass123"
    }')

HTTP_STATUS=$(echo "$LOGIN_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$LOGIN_RESPONSE" | head -n -1)
print_response "Connexion utilisateur" "$HTTP_STATUS" "$RESPONSE_BODY"

# Extraire le token
TOKEN=$(echo "$RESPONSE_BODY" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}❌ Impossible de récupérer le token${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Token récupéré: ${TOKEN:0:20}...${NC}"

# Test 3: Création d'un client
echo -e "\n${YELLOW}👥 TEST DE CRÉATION DE CLIENT${NC}"
CLIENT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/clients/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d '{
        "nom": "Entreprise Test CURL",
        "email": "contact@testcurl.com",
        "telephone": "0123456789",
        "adresse": "123 Rue Test CURL",
        "code_postal": "75001",
        "ville": "Paris",
        "statut": "actif"
    }')

HTTP_STATUS=$(echo "$CLIENT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$CLIENT_RESPONSE" | head -n -1)
print_response "Création client" "$HTTP_STATUS" "$RESPONSE_BODY"

# Extraire l'ID du client
CLIENT_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ -z "$CLIENT_ID" ]; then
    echo -e "${RED}❌ Impossible de récupérer l'ID du client${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Client créé avec l'ID: $CLIENT_ID${NC}"

# Test 4: Récupération de la liste des clients
echo -e "\n${YELLOW}📋 TEST DE LISTE DES CLIENTS${NC}"
LIST_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/clients/" \
    -H "Authorization: Token $TOKEN")

HTTP_STATUS=$(echo "$LIST_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$LIST_RESPONSE" | head -n -1)
print_response "Liste des clients" "$HTTP_STATUS" "$RESPONSE_BODY"

# Test 5: Récupération d'un client spécifique
echo -e "\n${YELLOW}🔍 TEST DE DÉTAIL CLIENT${NC}"
DETAIL_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/clients/$CLIENT_ID/" \
    -H "Authorization: Token $TOKEN")

HTTP_STATUS=$(echo "$DETAIL_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$DETAIL_RESPONSE" | head -n -1)
print_response "Détail du client $CLIENT_ID" "$HTTP_STATUS" "$RESPONSE_BODY"

# Test 6: Création d'un projet
echo -e "\n${YELLOW}📋 TEST DE CRÉATION DE PROJET${NC}"
PROJET_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/projets/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d "{
        \"titre\": \"Projet Test CURL\",
        \"description\": \"Projet de test pour l'API REST avec CURL\",
        \"client\": $CLIENT_ID,
        \"date_debut\": \"$(date +%Y-%m-%d)\",
        \"date_fin\": \"$(date -d '+30 days' +%Y-%m-%d)\",
        \"montant\": 5000.00,
        \"statut\": \"en_cours\"
    }")

HTTP_STATUS=$(echo "$PROJET_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$PROJET_RESPONSE" | head -n -1)
print_response "Création projet" "$HTTP_STATUS" "$RESPONSE_BODY"

# Extraire l'ID du projet
PROJET_ID=$(echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ -z "$PROJET_ID" ]; then
    echo -e "${RED}❌ Impossible de récupérer l'ID du projet${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Projet créé avec l'ID: $PROJET_ID${NC}"

# Test 7: Statistiques des projets
echo -e "\n${YELLOW}📊 TEST DES STATISTIQUES PROJETS${NC}"
STATS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/projets/stats/" \
    -H "Authorization: Token $TOKEN")

HTTP_STATUS=$(echo "$STATS_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$STATS_RESPONSE" | head -n -1)
print_response "Statistiques des projets" "$HTTP_STATUS" "$RESPONSE_BODY"

# Test 8: Création d'une facture
echo -e "\n${YELLOW}💰 TEST DE CRÉATION DE FACTURE${NC}"
FACTURE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/factures/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d "{
        \"client\": $CLIENT_ID,
        \"projet\": $PROJET_ID,
        \"montant\": 2500.00,
        \"date_emission\": \"$(date +%Y-%m-%d)\",
        \"date_echeance\": \"$(date -d '+30 days' +%Y-%m-%d)\",
        \"statut_paiement\": \"envoyée\"
    }")

HTTP_STATUS=$(echo "$FACTURE_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$FACTURE_RESPONSE" | head -n -1)
print_response "Création facture" "$HTTP_STATUS" "$RESPONSE_BODY"

# Test 9: Recherche dans les clients
echo -e "\n${YELLOW}🔍 TEST DE RECHERCHE${NC}"
SEARCH_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/clients/?search=CURL" \
    -H "Authorization: Token $TOKEN")

HTTP_STATUS=$(echo "$SEARCH_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$SEARCH_RESPONSE" | head -n -1)
print_response "Recherche de clients contenant 'CURL'" "$HTTP_STATUS" "$RESPONSE_BODY"

# Test 10: Test sans authentification (doit échouer)
echo -e "\n${YELLOW}🚫 TEST SANS AUTHENTIFICATION${NC}"
NO_AUTH_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/clients/")

HTTP_STATUS=$(echo "$NO_AUTH_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$NO_AUTH_RESPONSE" | head -n -1)
print_response "Accès sans authentification" "$HTTP_STATUS" "$RESPONSE_BODY"

echo -e "\n${GREEN}✅ TOUS LES TESTS SONT TERMINÉS !${NC}"
echo -e "\n📚 Pour plus de tests, utilisez l'interface Swagger :"
echo -e "   http://127.0.0.1:8000/api/v1/docs/" 