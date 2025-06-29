#!/bin/bash

# Script d'entrée pour l'application Django

set -e

# Attendre que la base de données soit prête
echo "Attente de la base de données..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "Base de données prête!"

# Attendre que Redis soit prête
echo "Attente de Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis prêt!"

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate

# Collecter les fichiers statiques (production uniquement)
if [ "$DEBUG" = "False" ]; then
    echo "Collecte des fichiers statiques..."
    python manage.py collectstatic --noinput
fi

# Créer un superuser si nécessaire (développement uniquement)
if [ "$DEBUG" = "True" ] && [ -z "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Création d'un superuser par défaut..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser créé: admin/admin123')
"
fi

# Exécuter la commande passée
exec "$@" 