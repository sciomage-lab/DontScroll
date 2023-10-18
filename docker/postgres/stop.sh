#!/bin/bash

docker-compose -f docker/postgres/docker-compose.yml down

docker volume ls

# docker volume rm postgres_pgadmin_data
if docker volume ls -q | grep -q 'postgres_pgadmin_data'; then
    docker volume rm postgres_pgadmin_data
else
    echo "No volume postgres_pgadmin_data"
fi

# docker volume rm postgres_postgresql_data
if docker volume ls -q | grep -q 'postgres_postgresql_data'; then
    docker volume rm postgres_postgresql_data
else
    echo "No volume postgres_postgresql_data"
fi
