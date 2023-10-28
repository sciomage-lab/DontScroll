#!/bin/bash
# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
#
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
#
# For more information, see the Sciomage LAB Public License which should accompany this project.


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
      -f ./docker/DontScroll/Dockerfile \
      -t dont-scroll:${tag} .
      # --no-cache \

# Run
docker-compose -f docker/DontScroll/docker-compose.yml up -d 
