#!/bin/bash

docker-compose down

docker volume ls
docker volume prune
