# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


import pytest

from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.core.utils import cos_sim


@pytest.mark.parametrize(
    "image1, image2, similarity",
    [
        ("./tests/images/hedgehog1.jpg", "./tests/images/hedgehog2.jpg", 0.75),
        ("./tests/images/cat1.png", "./tests/images/cat2.jpg", 0.75),
    ],
)
def test_similar_images(image1, image2, similarity):
    """
    Similar images
    """

    image_retrieval = ImageRetrieval()
    a = image_retrieval.image_to_vector(image1)
    b = image_retrieval.image_to_vector(image2)

    ret = cos_sim(a, b)
    assert similarity < ret


@pytest.mark.parametrize(
    "image1, image2, similarity",
    [
        ("./tests/images/hedgehog1.jpg", "./tests/images/cat1.png", 0.80),
        ("./tests/images/hedgehog1.jpg", "./tests/images/cat2.jpg", 0.80),
        ("./tests/images/hedgehog2.jpg", "./tests/images/cat1.png", 0.80),
        ("./tests/images/hedgehog2.jpg", "./tests/images/cat2.jpg", 0.80),
    ],
)
def test_different_images(image1, image2, similarity):
    """
    Different images
    """

    image_retrieval = ImageRetrieval()
    a = image_retrieval.image_to_vector(image1)
    b = image_retrieval.image_to_vector(image2)

    ret = cos_sim(a, b)
    assert ret < similarity


if __name__ == "__main__":
    test_similar_images()
    test_different_images()
