#!/bin/bash
# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
#
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
#
# For more information, see the Sciomage LAB Public License which should accompany this project.


docker build -f ./docker/postgres/Dockerfile -t cube-postgres:13 .
docker-compose -f docker/postgres/docker-compose.yml up -d
