#!/bin/bash

tag=0.1.1

      # --no-cache \
docker build \
      --progress=plain \
      -f Dockerfile \
      -t dont-scroll:${tag} .

docker-compose up -d
