# Mini CRM

[![Tests](https://github.com/labosnie/mini-crm/actions/workflows/django.yml/badge.svg)](https://github.com/labosnie/mini-crm/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un mini CRM développé avec Django pour gérer vos clients, projets et factures.

## Fonctionnalités

- Gestion des clients
- Gestion des projets
- Gestion des factures
- Tableau de bord interactif
- Export des données en CSV et PDF

## Technologies utilisées

- [Django](https://www.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Chart.js](https://www.chartjs.org/)

## Installation

1. Cloner le repository

```bash
git clone https://github.com/labosnie/mini-crm.git
cd mini-crm
```

2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
```

4. Configurer la base de données

```bash
python manage.py migrate
```

5. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

6. Lancer le serveur

```bash
python manage.py runserver
```

## Tests

Pour exécuter les tests :

```bash
python manage.py test
```

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
