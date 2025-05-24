# Mini CRM pour Freelance

Un système de gestion de clientèle simple et efficace pour les freelances.

## Structure du Projet

- `clients/` : Gestion des clients et contacts
- `projets/` : Suivi des projets
- `factures/` : Gestion des factures
- `dashboard/` : Tableau de bord principal

## Installation

1. Cloner le repository
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer l'environnement virtuel :
   - Windows : `.\venv\Scripts\activate`
   - Linux/Mac : `source venv/bin/activate`
4. Installer les dépendances : `pip install -r requirements.txt`
5. Effectuer les migrations : `python manage.py migrate`
6. Lancer le serveur : `python manage.py runserver`

## Fonctionnalités

- Gestion des clients
- Suivi des projets
- Gestion des factures
- Tableau de bord personnalisé
- Authentification des utilisateurs
