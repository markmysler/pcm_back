#!/bin/bash
set -e

# Charger les variables d'environnement
set -a
source /docker-entrypoint-initdb.d/.env
source /docker-entrypoint-initdb.d/.env.keycloak
set +a

echo "Starting database initialization..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
-- Créer l'utilisateur pour l'API s'il n'existe pas
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$API_DB_USER') THEN
    CREATE USER $API_DB_USER WITH PASSWORD '$API_DB_PASSWORD';
  END IF;
END
\$\$;

-- Créer l'utilisateur pour Keycloak s'il n'existe pas
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$KC_DB_USERNAME') THEN
    CREATE USER $KC_DB_USERNAME WITH PASSWORD '$KC_DB_PASSWORD';
  END IF;
END
\$\$;

-- Créer la base de données pour l'API si elle n'existe pas
CREATE DATABASE $API_DB_NAME;
GRANT ALL PRIVILEGES ON DATABASE $API_DB_NAME TO $API_DB_USER;

-- Créer la base de données pour Keycloak si elle n'existe pas
CREATE DATABASE $KC_DB_NAME;
GRANT ALL PRIVILEGES ON DATABASE $KC_DB_NAME TO $KC_DB_USERNAME;

-- Configurer la base de données de l'API
\c $API_DB_NAME
GRANT ALL ON SCHEMA public TO $API_DB_USER;
ALTER DEFAULT PRIVILEGES FOR ROLE $POSTGRES_USER IN SCHEMA public GRANT ALL ON TABLES TO $API_DB_USER;
ALTER DEFAULT PRIVILEGES FOR ROLE $POSTGRES_USER IN SCHEMA public GRANT ALL ON SEQUENCES TO $API_DB_USER;
ALTER DEFAULT PRIVILEGES FOR ROLE $POSTGRES_USER IN SCHEMA public GRANT ALL ON FUNCTIONS TO $API_DB_USER;
ALTER SCHEMA public OWNER TO $API_DB_USER;

-- Configurer la base de données de Keycloak
\c $KC_DB_NAME
GRANT ALL ON SCHEMA public TO $KC_DB_USERNAME;
ALTER DEFAULT PRIVILEGES FOR ROLE $POSTGRES_USER IN SCHEMA public GRANT ALL ON TABLES TO $KC_DB_USERNAME;
ALTER DEFAULT PRIVILEGES FOR ROLE $POSTGRES_USER IN SCHEMA public GRANT ALL ON SEQUENCES TO $KC_DB_USERNAME;
ALTER DEFAULT PRIVILEGES FOR ROLE $POSTGRES_USER IN SCHEMA public GRANT ALL ON FUNCTIONS TO $KC_DB_USERNAME;
ALTER SCHEMA public OWNER TO $KC_DB_USERNAME;
EOSQL

echo "Database initialization completed."