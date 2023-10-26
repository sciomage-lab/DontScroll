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

      # --no-cache \
docker build \
      --progress=plain \
      -f Dockerfile \
      -t dont-scroll:${tag} .
