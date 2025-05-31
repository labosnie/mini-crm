mini-CRM
Une application Django légère pour les freelances, permettant de gérer :

Les clients,

Les projets,

Les factures (avec numéros automatiques et dates d’échéance),

L’export de toutes les factures au format CSV ou PDF.

📋 Table des matières
Fonctionnalités

Installation

Configuration

Utilisation

Authentification

Clients

Projets

Factures

Export CSV / PDF

Personnalisation

Contribuer

Licence

🔥 Fonctionnalités
Gestion des clients

Création, modification, suppression, recherche, pagination

Upload facultatif de document (contrat, fichier PDF, etc.)

Gestion des projets

Lier un projet à un client

Statut (Planifié, En cours, Terminé)

Dates de début / de fin, priorité, validation métier (date de fin ≥ date de début)

Gestion des factures

Numéro de facture généré automatiquement (ex : 2025-001, 2025-002, …)

Date d’émission automatique à la création

Date d’échéance configurable

Montant, statut de paiement (Envoyée, Payée, En retard)

Validation : montant positif + cohérence client/projet

Recherche et filtres sur toutes les listes (clients, projets, factures)

Pagination (10 éléments par page par défaut)

Page d’accueil (Dashboard) avec navigation vers chaque section

Export :

CSV : télécharge un fichier CSV listant toutes les factures

PDF : génère un fichier PDF contenant toutes les factures

Interface responsive avec Bootstrap 5

Authentification et gestion des utilisateurs via django-allauth

Permissions :

Les utilisateurs ne voient et n’éditent que leurs propres clients/projets/factures

Seuls les administrateurs peuvent supprimer définitivement un enregistrement

📥 Installation
Clone le dépôt :

bash
Copier
Modifier
git clone https://github.com/labosnie/mini-crm.git
cd mini-crm
Crée et active un virtualenv (recommandé) :

bash
Copier
Modifier
python3 -m venv venv
source venv/bin/activate # Linux/macOS  
venv\Scripts\activate.ps1 # Windows PowerShell
Installe les dépendances :

bash
Copier
Modifier
pip install -r requirements.txt
Applique les migrations de la base de données :

bash
Copier
Modifier
python manage.py migrate
Crée un super-user Django (pour accéder à l’admin) :

bash
Copier
Modifier
python manage.py createsuperuser
Lance le serveur de développement :

bash
Copier
Modifier
python manage.py runserver
Ouvre ton navigateur à l’adresse http://127.0.0.1:8000/ pour accéder à l’application.

L’admin Django est disponible sur /admin/.

⚙️ Configuration
Clé secrète et DEBUG
Si tu veux configurer en mode production, pense à définir les variables d’environnement :

bash
Copier
Modifier
export DJANGO_SECRET_KEY='TaCléSecrèteIci'
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS='ton_domaine.com'
Stockage des fichiers
Les documents clients (contrats, PDF joints) sont sauvegardés dans MEDIA_ROOT.
Dans settings.py, tu peux définir :

python
Copier
Modifier
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
Pour servir ces fichiers en mode développement :

python
Copier
Modifier
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
🚀 Utilisation
Authentification
En mode développement, rends-toi sur /accounts/login/ pour te connecter (ou /accounts/signup/ pour créer un nouveau compte).

Si tu es super-user, tu peux aussi accéder à l’admin (/admin/) pour manipuler directement les données.

Clients
Clique sur Clients dans la barre de navigation.

Si aucun client n’existe, la liste est vide – clique sur Ajouter un client.

Renseigne :

Nom

Email

Téléphone (facultatif)

Adresse (facultatif)

Statut (Prospect, Client, Inactif)

Documents (upload d’un fichier PDF ou image – facultatif)

Clique sur Enregistrer : ton client apparaît dans la liste.

Tu peux rechercher par nom ou email, filtrer par statut, et naviguer par pagination (10 clients par page).

Pour modifier, clique sur l’icône ✏️ ; pour supprimer, clique sur l’icône 🗑️ (cet enregistrement sera définitivement supprimé).

Projets
Clique sur Projets dans la barre de navigation.

Ajouter un projet :

Titre

Client (sélectionne dans la liste des clients existants)

Description (facultatif)

Statut (Planifié, En cours, Terminé)

Date de début

Date de fin (facultative, mais si renseignée, doit être ≥ date de début)

Priorité (Haute, Moyenne, Basse)

Enregistrer : ton projet apparaît dans la liste.

Recherche, filtres (par statut / priorité) et pagination sont disponibles.

Factures
Clique sur Factures dans la barre de navigation.

Ajouter une facture :

Client (pré-rempli si le seul client possible)

Projet (ne liste que les projets du client sélectionné)

Numéro de facture (généré automatiquement, format YYYY-XXX)

Montant (doit être un nombre positif)

Date d’échéance (date limite de paiement)

Statut de paiement (par défaut “Envoyée”)

Notes (facultatif)

Enregistrer : la facture apparaît dans la liste, avec :

Numéro (ex : 2025-001, 2025-002, …)

Client

Projet

Montant (formaté en euros)

Date d’émission affichée au format jj/mm/aaaa

Date d’échéance (ou “–” si non renseignée)

Statut (“Envoyée”, “Payée”, “En retard”)

Recherche par numéro de facture ou nom du client, filtres par client / statut / date début / date fin, et pagination (10 factures par page).

➕ Export CSV / PDF
Exporter en CSV
Dans la page Liste des Factures, clique sur le bouton Exporter CSV (bouton vert).

Un fichier factures.csv est généré et téléchargé automatiquement.

Il contient : Numéro, Client, Projet, Montant, Date d’émission, Date d’échéance, Statut.

Exporter en PDF
Dans la même page, clique sur Exporter PDF (bouton rouge).

Le fichier factures.pdf est généré (grâce à WeasyPrint) et téléchargé.

Il affiche un tableau formaté reprenant les mêmes colonnes que le CSV, avec le style Bootstrap repris.

🛠️ Personnalisation
Changer le nombre de résultats par page
Dans clients/views.py, modifie paginate_by = 10 à la valeur souhaitée. Idem pour ProjetListView et FactureListView.

Modifier le format de numérotation automatique des factures
Le code se trouve dans factures/models.py (méthode save() ou utilitaire get_next_numero()). Adapte le format YYYY-XXX selon tes besoins (par ex. FAC-XXXX, etc.).

Configurer le style CSS
Par défaut, on utilise le CDN Bootstrap 5. Tu peux ajouter ton propre fichier CSS dans static/css/ et l’inclure dans base.html.

🤝 Contribuer
Fork le projet sur GitHub.

Crée une branche (git checkout -b feature/ma-fonctionnalité).

Commit tes changements (git commit -m "Ajout de la fonctionnalité X").

Push ta branche (git push origin feature/ma-fonctionnalité).

Ouvre une Pull Request.
