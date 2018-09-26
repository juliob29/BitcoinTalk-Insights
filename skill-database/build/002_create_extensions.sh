#!/bin/bash

set -e

#
#  Perform all actions as $POSTGRES_USER
#
export PGUSER="$POSTGRES_USER"
EXTENSIONS=('uuid-ossp' 'timescaledb' 'file_fdw')

#
#  Load extensions into both databases.
#  Only the PostGIS extensions are required
#  to be loaded into the template_postgis
#  template database. 
#
for EXT in "${EXTENSIONS[@]}"; do
    for DB in "$POSTGRES_DB"; do

echo "Loading $EXT extension into $DB"
psql --dbname="$DB" <<EOSQL
    CREATE EXTENSION IF NOT EXISTS "$EXT";
EOSQL

    done
done

echo "Creating csv_fdw server."
psql --dbname="$POSTGRES_DB" <<EOSQL
    CREATE SERVER csv_fdw
        FOREIGN DATA WRAPPER file_fdw;
EOSQL
