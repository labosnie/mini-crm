-- Script d'initialisation de la base de données
-- Donner les privilèges à l'utilisateur sur la base de données actuelle

-- Donner les privilèges à l'utilisateur
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO crm_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO crm_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO crm_user;

-- Créer les extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; 