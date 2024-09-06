#!/bin/sh

if [ ! -f /pgadmin4/servers.json ]; then
    touch /pgadmin4/servers.json
    chmod 666 /pgadmin4/servers.json
fi

envsubst < /pgadmin4/servers.template.json > /pgadmin4/servers.json
exec /entrypoint.sh "$@"
