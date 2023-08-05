#!/bin/bash

docker build -t cude-postgres:13 .
docker-compose up -d
