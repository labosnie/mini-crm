# Script PowerShell pour déployer sur Render

Write-Host "🚀 Déploiement sur Render..." -ForegroundColor Green

# Vérifier que git est configuré
if (-not (git config user.name)) {
    Write-Host "❌ Git n'est pas configuré. Veuillez configurer votre nom et email :" -ForegroundColor Red
    Write-Host "git config --global user.name 'Votre Nom'" -ForegroundColor Yellow
    Write-Host "git config --global user.email 'votre.email@example.com'" -ForegroundColor Yellow
    exit 1
}

# Ajouter tous les fichiers modifiés
Write-Host "📁 Ajout des fichiers modifiés..." -ForegroundColor Cyan
git add .

# Créer un commit
Write-Host "💾 Création du commit..." -ForegroundColor Cyan
$commitMessage = "Fix CSRF et configuration de sécurité pour Render - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
git commit -m $commitMessage

# Pousser vers le repository distant
Write-Host "📤 Push vers le repository distant..." -ForegroundColor Cyan
git push origin main

Write-Host "✅ Déploiement terminé !" -ForegroundColor Green
Write-Host "🌐 Votre application sera mise à jour sur Render dans quelques minutes." -ForegroundColor Cyan
Write-Host "🔗 URL : https://mini-crm-lezi.onrender.com" -ForegroundColor Cyan 