# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


import os

import numpy as np
from numpy import dot
from numpy.linalg import norm


def exist_file(path: str):
    return os.path.isfile(path)


def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))
