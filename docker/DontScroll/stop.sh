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

# docker volume rm dontscroll_dont_scroll_data
if docker volume ls -q | grep -q 'dontscroll_dont_scroll_data'; then
    docker volume rm dontscroll_dont_scroll_data
else
    echo "No volume dontscroll_dont_scroll_data"
fi
