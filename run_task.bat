@echo off
cd /d %~dp0
echo %date% %time% - Démarrage de la tâche >> task_log.txt
python manage_tasks.py >> task_log.txt 2>&1
echo %date% %time% - Fin de la tâche >> task_log.txt
echo. >> task_log.txt 