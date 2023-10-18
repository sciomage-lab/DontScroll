#!/bin/bash

tag=0.1.1

if [ -z "$SLACK_SIGNING_SECRET" ]; then
  echo "SLACK_SIGNING_SECRET is null"
  exit 1
fi

if [ -z "$BOT_USER_OAUTH_TOKEN" ]; then
  echo "BOT_USER_OAUTH_TOKEN is null"
  exit 1
fi

if [ -z "$SLACK_APP_TOKEN" ]; then
  echo "SLACK_APP_TOKEN is null"
  exit 1
fi

if [ -z "$CHANNEL_ID" ]; then
  echo "CHANNEL_ID is null"
  exit 1
fi

# Build
docker build \
      --progress=plain \
      -f ./docker/DontScroll/Dockerfile \
      -t dont-scroll:${tag} .
      # --no-cache \

# Run
docker-compose -f docker/DontScroll/docker-compose.yml up -d 
