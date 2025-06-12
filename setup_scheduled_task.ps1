# Obtenir le chemin absolu du répertoire courant
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$taskPath = Join-Path $scriptPath "run_task.bat"

# Créer l'action pour la tâche planifiée
$action = New-ScheduledTaskAction -Execute $taskPath

# Créer le déclencheur pour exécution quotidienne à 9h00
$trigger = New-ScheduledTaskTrigger -Daily -At 9AM

# Créer les paramètres de la tâche
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

# Créer la tâche planifiée
Register-ScheduledTask -TaskName "RelanceFacturesCRM" -Action $action -Trigger $trigger -Settings $settings -Description "Relance automatique des factures en retard" -Force

Write-Host "Tâche planifiée 'RelanceFacturesCRM' créée avec succès. Elle s'exécutera tous les jours à 9h00." 