#!/bin/bash

docker-compose down

docker volume ls
docker volume rm postgres_pgadmin_data
docker volume rm postgres_postgresql_data
