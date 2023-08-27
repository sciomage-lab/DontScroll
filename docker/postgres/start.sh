#!/bin/bash

docker build -t cube-postgres:13 .
docker-compose up -d
