#!/usr/bin/env bash

# Configure postgres Container image pgvector/pgvector:pg17 to listen on 127.0.0.1
# Mount this file into container:/docker-entrypoint-initdb.d/

CONFIG="/var/lib/postgresql/data/postgresql.conf"

echo '[pgvector-init] Ensure listen_addresses is 127.0.0.1 ...'

if [ ! -f "${CONFIG}" ]; then
	echo '[pgvector-init] ${CONFIG} missing! Waiting here.'
	sleep infinity
fi

if grep -qE "^listen_addresses = '127.0.0.1'" ${CONFIG}; then
	echo '[pgvector-init] All fine.'
else
	echo "listen_addresses = '127.0.0.1'" >> ${CONFIG}
	echo '[pgvector-init] Configued.'
fi

echo '[pgvector-init] Done.'
