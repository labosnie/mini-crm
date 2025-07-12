# Mini CRM

[![Tests](https://github.com/labosnie/mini-crm/actions/workflows/django.yml/badge.svg)](https://github.com/labosnie/mini-crm/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un mini CRM développé avec Django pour gérer vos clients, projets et factures avec une API REST complète et une documentation interactive.

## 🚀 Fonctionnalités

### Interface Web

- **Gestion des clients** : CRUD complet avec tags et interactions
- **Gestion des projets** : Suivi des projets par client
- **Gestion des factures** : Création, suivi et relances automatiques
- **Tableau de bord interactif** : KPIs et graphiques en temps réel
- **Export des données** : CSV et PDF
- **Interface responsive** : Optimisée pour tous les appareils

### API REST

- **API complète** : Endpoints pour clients, projets, factures et authentification
- **Authentification sécurisée** : Token-based authentication
- **Permissions granulaires** : Contrôle d'accès par utilisateur
- **Filtrage et recherche** : API flexible avec filtres avancés
- **Pagination** : Gestion optimisée des grandes listes
- **Documentation interactive** : Swagger/OpenAPI intégré

### Fonctionnalités avancées

- **Relances automatiques** : Système de relance des factures en retard
- **Génération PDF** : Factures générées automatiquement
- **Tests automatisés** : Couverture complète des tests
- **Tâches asynchrones** : Celery pour les tâches en arrière-plan

## 🛠️ Technologies utilisées

### Backend

- [Django](https://www.djangoproject.com/) - Framework web
- [Django REST Framework](https://www.django-rest-framework.org/) - API REST
- [PostgreSQL](https://www.postgresql.org/) - Base de données
- [Celery](https://celeryproject.org/) - Tâches asynchrones
- [ReportLab](https://www.reportlab.com/) - Génération PDF

### Infrastructure

- [Docker](https://www.docker.com/) - Conteneurisation
- [Docker Compose](https://docs.docker.com/compose/) - Orchestration multi-services
- [Redis](https://redis.io/) - Cache et broker de messages

### Frontend

- [Bootstrap 5](https://getbootstrap.com/) - Framework CSS
- [Chart.js](https://www.chartjs.org/) - Graphiques
- [jQuery](https://jquery.com/) - Manipulation DOM

### Documentation & Tests

- [drf-spectacular](https://drf-spectacular.readthedocs.io/) - Documentation API
- [pytest](https://pytest.org/) - Framework de tests
- [coverage](https://coverage.readthedocs.io/) - Couverture de code

## 📦 Installation

### Option 1 : Installation avec Docker (Recommandée)

#### Prérequis

- Docker et Docker Compose

#### Démarrage rapide

```bash
# Cloner le repository
git clone https://github.com/labosnie/mini-crm.git
cd mini-crm

# Lancer tous les services
docker-compose up -d

# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# Accéder à l'application
# http://localhost:8000
```

#### Services Docker inclus

- **Web** : Application Django (port 8000)
- **PostgreSQL** : Base de données (port 5432)
- **Redis** : Cache et broker Celery (port 6379)
- **Celery** : Worker pour tâches asynchrones
- **Celery Beat** : Planificateur de tâches

### Option 2 : Installation locale

#### Prérequis

- Python 3.8+
- PostgreSQL
- Redis (pour Celery)

### 1. Cloner le repository

```bash
git clone https://github.com/labosnie/mini-crm.git
cd mini-crm
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

Créer un fichier `.env` à la racine du projet :

```env
DEBUG=True
SECRET_KEY=votre-clé-secrète
DATABASE_URL=postgresql://user:password@localhost:5432/mini_crm
REDIS_URL=redis://localhost:6379/0
```

### 5. Configurer la base de données

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 7. Lancer les services

```bash
# Terminal 1 : Serveur Django
python manage.py runserver

# Terminal 2 : Worker Celery (optionnel)
celery -A mini_crm worker -l info

# Terminal 3 : Beat Celery pour les tâches planifiées (optionnel)
celery -A mini_crm beat -l info
```

### Commandes Docker utiles

```bash
# Voir les logs
docker-compose logs -f web

# Redémarrer un service
docker-compose restart web

# Arrêter tous les services
docker-compose down

# Reconstruire l'image
docker-compose build

# Accéder au shell du conteneur
docker-compose exec web bash
```

## 🔧 Configuration

### Variables d'environnement

| Variable        | Description                 | Défaut                |
| --------------- | --------------------------- | --------------------- |
| `DEBUG`         | Mode debug                  | `True`                |
| `SECRET_KEY`    | Clé secrète Django          | -                     |
| `DATABASE_URL`  | URL de connexion PostgreSQL | -                     |
| `REDIS_URL`     | URL Redis pour Celery       | -                     |
| `ALLOWED_HOSTS` | Hôtes autorisés             | `localhost,127.0.0.1` |

### Configuration Celery

Les tâches asynchrones incluent :

- Relances automatiques des factures en retard
- Génération de rapports PDF
- Envoi d'emails de notification

## 📚 API Documentation

### Accès à la documentation

Une fois le serveur lancé, accédez à :

- **Interface Swagger** : http://127.0.0.1:8000/api/v1/docs/
- **Documentation OpenAPI** : http://127.0.0.1:8000/api/v1/schema/
- **Documentation ReDoc** : http://127.0.0.1:8000/api/v1/redoc/

### Authentification API

```bash
# Obtenir un token
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "votre_username", "password": "votre_password"}'

# Utiliser le token
curl -X GET http://127.0.0.1:8000/api/v1/clients/ \
  -H "Authorization: Token votre_token_ici"
```

### Endpoints principaux

| Endpoint            | Description      | Méthodes               |
| ------------------- | ---------------- | ---------------------- |
| `/api/v1/auth/`     | Authentification | POST                   |
| `/api/v1/clients/`  | Gestion clients  | GET, POST, PUT, DELETE |
| `/api/v1/projets/`  | Gestion projets  | GET, POST, PUT, DELETE |
| `/api/v1/factures/` | Gestion factures | GET, POST, PUT, DELETE |

## 🧪 Tests

### Exécuter tous les tests

```bash
python manage.py test
```

### Tests spécifiques

```bash
# Tests de l'API
python manage.py test api.tests

# Tests des clients
python manage.py test clients.test

# Tests des factures
python manage.py test factures.test

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
coverage html  # Génère un rapport HTML
```

### Tests API avec curl

```bash
# Script de test automatique
./test_api_curl.sh
```

## 📊 Fonctionnalités avancées

### Dashboard

Le tableau de bord affiche :

- Nombre total de clients, projets et factures
- Montant total des factures
- Graphique des factures par mois
- KPIs en temps réel

### Relances automatiques

Le système vérifie quotidiennement les factures en retard et :

- Envoie des notifications automatiques
- Met à jour le statut des factures
- Génère des rapports de relance

### Export de données

- **CSV** : Export complet des données
- **PDF** : Rapports formatés professionnellement
- **Factures PDF** : Génération automatique des factures

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

Pour toute question ou problème :

- Ouvrir une issue sur GitHub
- Consulter la documentation API
- Vérifier les logs du serveur

## 🔄 Changelog

### Version 2.0.0

- ✅ API REST complète avec Django REST Framework
- ✅ Documentation Swagger/OpenAPI interactive
- ✅ Tests automatisés complets
- ✅ Authentification Token sécurisée
- ✅ Système de relances automatiques
- ✅ Génération PDF des factures
- ✅ Dashboard enrichi avec KPIs

### Version 1.0.0

- ✅ Interface web de base
- ✅ Gestion CRUD des entités
- ✅ Export CSV/PDF
- ✅ Interface responsive
