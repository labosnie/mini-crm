-- Script d'initialisation de la base de données
-- Créer l'utilisateur et la base de données si nécessaire

-- Créer l'utilisateur (déjà fait par les variables d'environnement)
-- GRANT ALL PRIVILEGES ON DATABASE crm_db TO crm_user;

-- Connexion à la base de données crm_db
\c crm_db;

-- Donner les privilèges à l'utilisateur
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO crm_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO crm_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO crm_user;

-- Créer les extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; 