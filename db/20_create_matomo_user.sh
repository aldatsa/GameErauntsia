#!/bin/bash

set -eu -o pipefail
mysql -uroot -p${MYSQL_ROOT_PASSWORD} <<EOF
CREATE DATABASE ${MATOMO_DATABASE_DBNAME};
CREATE USER ${MATOMO_DATABASE_USERNAME}@'%' IDENTIFIED BY '${MATOMO_DATABASE_PASSWORD}';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, DROP, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES ON ${MATOMO_DATABASE_DBNAME}.* TO ${MATOMO_DATABASE_USERNAME}@'%';
EOF