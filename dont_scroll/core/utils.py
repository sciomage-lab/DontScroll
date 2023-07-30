import os
import numpy as np
from numpy import dot
from numpy.linalg import norm

def exist_file(path: str):
    return os.path.isfile(path)


def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))
