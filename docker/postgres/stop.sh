#!/bin/bash
# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
#
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
#
# For more information, see the Sciomage LAB Public License which should accompany this project.


docker-compose down

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
