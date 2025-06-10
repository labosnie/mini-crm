# Mini-CRM

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/votre-username/mini-crm)
[![Tests](https://github.com/labosnie/mini-crm/actions/workflows/django.yml/badge.svg)](https://github.com/labosnie/mini-crm/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un système de gestion de la relation client (CRM) léger et efficace, développé avec Django.

## 🚀 Fonctionnalités

### Gestion des Clients

- Création et gestion des profils clients
- Suivi des interactions
- Système de tags personnalisables
- Export des données (CSV/PDF)

### Gestion des Projets

- Suivi des projets par client
- Statuts personnalisables
- Dates de début et de fin
- Montants et budgets

### Gestion des Factures

- Numérotation automatique
- Suivi des paiements
- Dates d'échéance
- Export des factures (CSV/PDF)

## 🛠️ Technologies Utilisées

- Python 3.13
- Django 5.2
- Bootstrap 5
- Font Awesome
- ReportLab (pour les exports PDF)

## 📋 Prérequis

- Python 3.13 ou supérieur
- pip (gestionnaire de paquets Python)
- Un environnement virtuel (recommandé)

## 🔧 Installation

1. Cloner le repository :

```bash
git clone https://github.com/votre-username/mini-crm.git
cd mini-crm
```

2. Créer et activer l'environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Configurer la base de données :

```bash
python manage.py migrate
```

5. Créer un superutilisateur :

```bash
python manage.py createsuperuser
```

6. Lancer le serveur de développement :

```bash
python manage.py runserver
```

## 📦 Structure du Projet

```
mini-crm/
├── clients/          # Application de gestion des clients
├── projets/          # Application de gestion des projets
├── factures/         # Application de gestion des factures
├── templates/        # Templates HTML
├── static/          # Fichiers statiques (CSS, JS, images)
└── manage.py        # Script de gestion Django
```

## 🔐 Sécurité

- Authentification requise pour toutes les fonctionnalités
- Protection CSRF sur tous les formulaires
- Validation des données côté serveur
- Gestion sécurisée des mots de passe

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème, veuillez :

- Ouvrir une issue sur GitHub
- Décrire clairement le problème
- Fournir les étapes pour reproduire le bug
- Inclure les messages d'erreur pertinents

# Mini CRM

![Tests](https://github.com/labosnie/mini-crm/actions/workflows/django.yml/badge.svg)

Un mini CRM développé avec Django pour gérer vos clients, projets et factures.
