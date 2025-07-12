# Guide de déploiement sur Render

## Problème CSRF résolu

L'erreur CSRF que vous rencontriez était due à une configuration manquante pour les domaines de production. Les corrections suivantes ont été apportées :

### 1. Configuration CSRF ajoutée

Dans `mini_crm/settings.py` :

```python
# Configuration CSRF pour la production
CSRF_TRUSTED_ORIGINS = [
    "https://mini-crm-lezi.onrender.com",
    "https://*.onrender.com",
]

# Configuration de sécurité pour la production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 2. Configuration CORS mise à jour

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://mini-crm-lezi.onrender.com",
]
```

### 3. Variables d'environnement Render

Dans `render.yaml`, ajout des variables :

```yaml
- key: CSRF_TRUSTED_ORIGINS
  value: https://mini-crm-lezi.onrender.com
- key: CORS_ALLOWED_ORIGINS
  value: https://mini-crm-lezi.onrender.com
```

## Déploiement

### Option 1 : Script automatique (Windows)

```powershell
.\scripts\deploy-render.ps1
```

### Option 2 : Script automatique (Linux/Mac)

```bash
chmod +x scripts/deploy-render.sh
./scripts/deploy-render.sh
```

### Option 3 : Commandes manuelles

```bash
# 1. Ajouter les fichiers modifiés
git add .

# 2. Créer un commit
git commit -m "Fix CSRF et configuration de sécurité pour Render"

# 3. Pousser vers le repository
git push origin main
```

## Vérification du déploiement

1. **Attendez 2-3 minutes** après le push pour que Render déploie les modifications
2. **Accédez à l'application** : https://mini-crm-lezi.onrender.com
3. **Testez la connexion** : https://mini-crm-lezi.onrender.com/accounts/login/

## Création d'un superutilisateur

Si vous n'avez pas encore de compte administrateur, vous pouvez en créer un via le shell Render :

```bash
# Dans le dashboard Render, allez dans votre service web
# Cliquez sur "Shell" et exécutez :
python manage.py createsuperuser
```

## Dépannage

### Si l'erreur CSRF persiste

1. Vérifiez que les variables d'environnement sont bien définies dans Render
2. Attendez quelques minutes supplémentaires pour le redéploiement
3. Videz le cache de votre navigateur

### Si la base de données n'est pas accessible

1. Vérifiez que la base de données PostgreSQL est bien créée dans Render
2. Vérifiez la variable `DATABASE_URL` dans les variables d'environnement

### Logs de déploiement

Vous pouvez consulter les logs de déploiement dans le dashboard Render :

1. Allez dans votre service web
2. Cliquez sur "Logs"
3. Vérifiez qu'il n'y a pas d'erreurs lors du déploiement

## Configuration de production

Pour une utilisation en production, assurez-vous de :

1. **Changer la clé secrète** : Render génère automatiquement une clé secrète sécurisée
2. **Désactiver le mode DEBUG** : `DEBUG=False` (déjà configuré)
3. **Configurer les variables d'environnement** : Toutes les variables nécessaires sont définies dans `render.yaml`

## Support

Si vous rencontrez encore des problèmes :

1. Consultez les logs dans le dashboard Render
2. Vérifiez que tous les fichiers ont été correctement déployés
3. Testez l'application en local pour isoler les problèmes
