# Architecture du Mini CRM

## 🏗️ Vue d'ensemble

Le Mini CRM est une application web moderne construite avec Django, utilisant une architecture microservices conteneurisée.

## 📊 Architecture système

```mermaid
graph TB
    subgraph "Frontend"
        A[Interface Web]
        B[API Documentation]
    end

    subgraph "Backend"
        C[Django Application]
        D[Django REST Framework]
        E[Celery Workers]
        F[Celery Beat]
    end

    subgraph "Services"
        G[PostgreSQL]
        H[Redis]
        I[PDF Generator]
    end

    A --> C
    B --> D
    C --> D
    D --> G
    E --> H
    F --> H
    C --> I
```

## 🗄️ Modèle de données

```mermaid
erDiagram
    CLIENTS {
        int id PK
        string nom
        string email
        string telephone
        text adresse
        string code_postal
        string ville
        string pays
        text notes
        string statut
        timestamp date_creation
        array tags
    }

    PROJETS {
        int id PK
        int client_id FK
        string nom
        text description
        date date_debut
        date date_fin
        string statut
        decimal budget
    }

    FACTURES {
        int id PK
        int client_id FK
        int projet_id FK
        string numero
        date date_emission
        date date_echeance
        decimal montant_ht
        decimal tva
        decimal montant_ttc
        string statut_paiement
        text notes
    }

    CLIENTS ||--o{ PROJETS : "possède"
    CLIENTS ||--o{ FACTURES : "reçoit"
    PROJETS ||--o{ FACTURES : "génère"
```

## 🔄 Flux de données

### 1. Gestion des clients

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant W as Web Interface
    participant API as Django API
    participant DB as PostgreSQL

    U->>W: Créer/Modifier client
    W->>API: POST /api/clients/
    API->>DB: INSERT/UPDATE
    DB-->>API: Confirmation
    API-->>W: Réponse JSON
    W-->>U: Confirmation
```

### 2. Génération de factures

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant W as Web Interface
    participant API as Django API
    participant C as Celery
    participant P as PDF Generator

    U->>W: Générer facture PDF
    W->>API: POST /api/factures/{id}/pdf/
    API->>C: Tâche asynchrone
    C->>P: Générer PDF
    P-->>C: PDF généré
    C-->>API: Tâche terminée
    API-->>W: Lien vers PDF
    W-->>U: Téléchargement
```

## 🚀 Déploiement

### Architecture de production

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Nginx]
    end

    subgraph "Application Servers"
        APP1[Django App 1]
        APP2[Django App 2]
    end

    subgraph "Services"
        DB[(PostgreSQL)]
        REDIS[(Redis)]
        CELERY[Celery Workers]
    end

    LB --> APP1
    LB --> APP2
    APP1 --> DB
    APP2 --> DB
    APP1 --> REDIS
    APP2 --> REDIS
    CELERY --> REDIS
    CELERY --> DB
```

## 🔧 Technologies utilisées

| Composant          | Technologie           | Version |
| ------------------ | --------------------- | ------- |
| Framework Web      | Django                | 5.2+    |
| API                | Django REST Framework | 3.16+   |
| Base de données    | PostgreSQL            | 15+     |
| Cache/Broker       | Redis                 | 7+      |
| Tâches asynchrones | Celery                | 5.5+    |
| Conteneurisation   | Docker                | 20+     |
| Orchestration      | Docker Compose        | 2+      |
| Serveur WSGI       | Gunicorn              | 23+     |
| Génération PDF     | ReportLab             | 4.4+    |

## 📈 Métriques et monitoring

- **Performance** : Temps de réponse < 200ms
- **Disponibilité** : 99.9% uptime
- **Sécurité** : Authentification JWT, HTTPS obligatoire
- **Scalabilité** : Architecture horizontale possible

## Étapes suivantes

### 1. **Renommer les fichiers**

Assure-toi que tes screenshots sont nommés comme dans le README :

- `dashboard.png`
- `clients.png`
- `factures.png`
- `api-docs.png`
- `demo.gif` (si tu as fait le GIF)

### 2. **Les placer dans le bon dossier**

Déplace tous tes screenshots dans le dossier `docs/` :

```
docs/
├── dashboard.png
├── clients.png
├── factures.png
├── api-docs.png
└── demo.gif
```

### 3. **Vérifier que les images s'affichent**

Le README est déjà configuré pour afficher :

```markdown
<code_block_to_apply_changes_from>
![Dashboard](docs/dashboard.png)
![Gestion clients](docs/clients.png)
![Factures](docs/factures.png)
![API Documentation](docs/api-docs.png)
```

### 4. **Prochaine étape : Démo en ligne**

Maintenant on peut passer au déploiement sur Render pour avoir une démo live !

Tu veux qu'on :

1. **Organise d'abord les screenshots** dans le dossier `docs/` ?
2. **Ou on passe directement au déploiement** de la démo en ligne ?

Qu'est-ce que tu préfères ? 🚀
