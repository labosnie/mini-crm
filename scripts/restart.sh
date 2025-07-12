#!/bin/bash

echo "🔄 Arrêt des conteneurs existants..."
docker-compose down

echo "🗑️  Suppression des volumes pour repartir de zéro..."
docker volume rm mini-crm_postgres_data mini-crm_redis_data 2>/dev/null || true

echo "🚀 Démarrage des conteneurs..."
docker-compose up -d

echo "⏳ Attente que PostgreSQL soit prêt..."
sleep 10

echo "📊 Application des migrations..."
docker-compose exec web python manage.py migrate

echo "👤 Création d'un superutilisateur..."
echo "Entrez les informations pour créer un superutilisateur :"
docker-compose exec web python manage.py createsuperuser

echo "✅ Application prête !"
echo "🌐 Accédez à l'application : http://localhost:8000"
echo "🔧 Interface d'administration : http://localhost:8000/admin/" 