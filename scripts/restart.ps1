# Script PowerShell pour redémarrer les conteneurs Docker

Write-Host "🔄 Arrêt des conteneurs existants..." -ForegroundColor Yellow
docker-compose down

Write-Host "🗑️  Suppression des volumes pour repartir de zéro..." -ForegroundColor Yellow
docker volume rm mini-crm_postgres_data, mini-crm_redis_data 2>$null

Write-Host "🚀 Démarrage des conteneurs..." -ForegroundColor Green
docker-compose up -d

Write-Host "⏳ Attente que PostgreSQL soit prêt..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

Write-Host "📊 Application des migrations..." -ForegroundColor Green
docker-compose exec web python manage.py migrate

Write-Host "👤 Création d'un superutilisateur..." -ForegroundColor Green
Write-Host "Entrez les informations pour créer un superutilisateur :" -ForegroundColor Cyan
docker-compose exec web python manage.py createsuperuser

Write-Host "✅ Application prête !" -ForegroundColor Green
Write-Host "🌐 Accédez à l'application : http://localhost:8000" -ForegroundColor Cyan
Write-Host "🔧 Interface d'administration : http://localhost:8000/admin/" -ForegroundColor Cyan 