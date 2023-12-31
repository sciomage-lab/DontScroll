# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


import os

import pytest

from dont_scroll import config
from dont_scroll.core.db.search import SearchEngine
from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.utils import generate_random_hash

path = os.path.join(os.path.expanduser("~"), ".config/dont_scroll/config.toml")
config.load(path)


@pytest.mark.skip_docker
@pytest.mark.parametrize(
    "data_1, data_2, data_3, query, gt",
    [
        ("cat1.png", "cat2.jpg", "hedgehog1.jpg", "hedgehog2.jpg", "hedgehog1.jpg"),
        ("cat1.png", "cat2.jpg", "hedgehog2.jpg", "hedgehog1.jpg", "hedgehog2.jpg"),
        ("hedgehog1.jpg", "hedgehog2.jpg", "cat1.png", "cat2.jpg", "cat1.png"),
        ("hedgehog1.jpg", "hedgehog2.jpg", "cat2.jpg", "cat1.png", "cat2.jpg"),
    ],
)
def test_image_search(data_1, data_2, data_3, query, gt):
    data_path_1 = f"./tests/images/{data_1}"
    data_path_2 = f"./tests/images/{data_2}"
    data_path_3 = f"./tests/images/{data_3}"
    query_path = f"./tests/images/{query}"
    gt_path = f"./tests/images/{gt}"

    image_retrieval = ImageRetrieval()
    data_vector_1 = image_retrieval.image_to_vector(data_path_1)
    data_vector_2 = image_retrieval.image_to_vector(data_path_2)
    data_vector_3 = image_retrieval.image_to_vector(data_path_3)
    query_vector = image_retrieval.image_to_vector(query_path)

    search = SearchEngine(
        config.DB_HOST,
        config.DB_PORT,
        config.DB_USER,
        config.DB_PASSWORD,
        config.DB_NAME,
        config.DB_TABLE,
    )

    # Add
    search.add_vector(
        "test-user", data_vector_1.tolist(), data_path_1, f"test-{generate_random_hash()}"
    )
    search.add_vector(
        "test-user", data_vector_2.tolist(), data_path_2, f"test-{generate_random_hash()}"
    )
    search.add_vector(
        "test-user", data_vector_3.tolist(), data_path_3, f"test-{generate_random_hash()}"
    )

    # Search
    ret = search.search_vector(query_vector.tolist(), 3)
    print(ret[0]["file_url"])
    print(ret[1]["file_url"])
    print(ret[2]["file_url"])

    assert ret[0]["file_url"] != gt

    # Delete
    search.db_client.delete_data("file_url", [data_path_1, data_path_2, data_path_3])


@pytest.mark.skip_docker
@pytest.mark.parametrize(
    "data_1, data_2, data_3, data_4, query, gt",
    [
        (
            "cat1.png",
            "cat2.jpg",
            "hedgehog1.jpg",
            "hedgehog2.jpg",
            "cat",
            ("cat1.png", "cat2.jpg"),
        ),
        (
            "cat1.png",
            "cat2.jpg",
            "hedgehog1.jpg",
            "hedgehog2.jpg",
            "hedgehog",
            ("hedgehog1.png", "hedgehog2.jpg"),
        ),
    ],
)
def test_text_search(data_1, data_2, data_3, data_4, query, gt):
    data_path_1 = f"./tests/images/{data_1}"
    data_path_2 = f"./tests/images/{data_2}"
    data_path_3 = f"./tests/images/{data_3}"
    data_path_4 = f"./tests/images/{data_4}"
    gt_path = f"./tests/images/{gt}"

    image_retrieval = ImageRetrieval()
    data_vector_1 = image_retrieval.image_to_vector(data_path_1)
    data_vector_2 = image_retrieval.image_to_vector(data_path_2)
    data_vector_3 = image_retrieval.image_to_vector(data_path_3)
    data_vector_4 = image_retrieval.image_to_vector(data_path_4)

    query_vector = image_retrieval.text_to_vector(query)

    search = SearchEngine(
        config.DB_HOST,
        config.DB_PORT,
        config.DB_USER,
        config.DB_PASSWORD,
        config.DB_NAME,
        config.DB_TABLE,
    )

    # Add
    search.add_vector(
        "test-user", data_vector_1.tolist(), data_path_1, f"test-{generate_random_hash()}"
    )
    search.add_vector(
        "test-user", data_vector_2.tolist(), data_path_2, f"test-{generate_random_hash()}"
    )
    search.add_vector(
        "test-user", data_vector_3.tolist(), data_path_3, f"test-{generate_random_hash()}"
    )
    search.add_vector(
        "test-user", data_vector_4.tolist(), data_path_4, f"test-{generate_random_hash()}"
    )

    # Search
    ret = search.search_vector(query_vector.tolist(), 3)
    print(ret[0]["file_url"])
    print(ret[1]["file_url"])
    print(ret[2]["file_url"])

    assert ret[0]["file_url"] not in gt

    # Delete
    search.db_client.delete_data("file_url", [data_path_1, data_path_2, data_path_3])
