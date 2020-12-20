#!/bin/bash
sudo apt-get --purge remove postgresql-*
sudo rm -Rf /etc/postgresql /var/lib/postgresql
sudo apt-get install postgresql
sudo su - postgres -c "createuser -s stach"
sudo su - postgres -c "createdb stach"
psql -c "CREATE EXTENSION file_fdw;"
psql -c "CREATE SERVER csv FOREIGN DATA WRAPPER file_fdw;"
psql -c "ALTER USER stach WITH PASSWORD 'pol0pol9';"
