#!/bin/bash
set -e

# Create n8n database and user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER n8n_user WITH PASSWORD 'IQjywSHgWCdYMLr0!#+49j@+BGfAl3W$';
    CREATE DATABASE n8n OWNER n8n_user;
    GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n_user;
EOSQL

echo "n8n database and user created successfully"
