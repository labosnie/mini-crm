# Guide de création des visuels

## 📸 Screenshots à capturer

### 1. Dashboard principal

- Capture du tableau de bord avec les KPIs
- Graphiques et statistiques visibles
- Interface moderne et professionnelle

### 2. Interface de gestion des clients

- Liste des clients avec filtres
- Formulaire d'ajout/modification
- Tags et interactions visibles

### 3. Gestion des factures

- Liste des factures avec statuts
- Formulaire de création de facture
- Boutons d'export PDF/CSV

### 4. Facture PDF générée

- Exemple de facture PDF exportée
- Mise en page professionnelle
- Logo et informations complètes

### 5. API Documentation

- Interface Swagger/OpenAPI
- Endpoints documentés
- Exemples de requêtes

## 🎬 GIF d'utilisation

### Scénario à filmer (10-20 secondes)

1. Connexion à l'application
2. Navigation rapide dashboard → clients → factures
3. Création d'une facture
4. Export PDF
5. Retour au dashboard

### Outils recommandés

- **Windows** : LICEcap, ShareX
- **Mac** : LICEcap, Kap
- **Linux** : Peek, Kazam

## 📊 Diagramme d'architecture

### Créer avec dbdiagram.io

```sql
// Modèle de base de données
Table clients {
  id integer [primary key]
  nom varchar
  email varchar
  telephone varchar
  adresse text
  code_postal varchar
  ville varchar
  pays varchar
  notes text
  statut varchar
  date_creation timestamp
  tags text[]
}

Table projets {
  id integer [primary key]
  client_id integer [ref: > clients.id]
  nom varchar
  description text
  date_debut date
  date_fin date
  statut varchar
  budget decimal
}

Table factures {
  id integer [primary key]
  client_id integer [ref: > clients.id]
  projet_id integer [ref: > projets.id]
  numero varchar
  date_emission date
  date_echeance date
  montant_ht decimal
  tva decimal
  montant_ttc decimal
  statut_paiement varchar
  notes text
}
```

## 🚀 Démo en ligne

### Configuration pour Render

1. Connecter le repo GitHub
2. Service Web avec Python
3. Base de données PostgreSQL
4. Variables d'environnement
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn mini_crm.wsgi:application`

### Compte démo

- Email: demo@example.com
- Mot de passe: demo123
- Accès en lecture seule
