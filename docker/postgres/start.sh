#!/bin/bash

docker build -f ./docker/postgres/Dockerfile -t cube-postgres:13 .
docker-compose -f docker/postgres/docker-compose.yml up -d
