#!/bin/bash

echo "🚀 Déploiement sur Render..."

# Vérifier que git est configuré
if ! git config user.name > /dev/null 2>&1; then
    echo "❌ Git n'est pas configuré. Veuillez configurer votre nom et email :"
    echo "git config --global user.name 'Votre Nom'"
    echo "git config --global user.email 'votre.email@example.com'"
    exit 1
fi

# Ajouter tous les fichiers modifiés
echo "📁 Ajout des fichiers modifiés..."
git add .

# Créer un commit
echo "💾 Création du commit..."
git commit -m "Fix CSRF et configuration de sécurité pour Render - $(date)"

# Pousser vers le repository distant
echo "📤 Push vers le repository distant..."
git push origin main

echo "✅ Déploiement terminé !"
echo "🌐 Votre application sera mise à jour sur Render dans quelques minutes."
echo "🔗 URL : https://mini-crm-lezi.onrender.com" 