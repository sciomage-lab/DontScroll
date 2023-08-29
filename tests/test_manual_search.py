import os

import pytest

from dont_scroll import config
from dont_scroll.core.db.search import SearchEngine
from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.utils import generate_random_hash

path = os.path.join(os.path.expanduser("~"), ".config/dont_scroll/config.toml")
config.load(path)


if __name__ == "__main__":
    image_retrieval = ImageRetrieval()

    query = "wedding invitation"
    query_vector = image_retrieval.text_to_vector(query)

    search = SearchEngine(
        config.DB_HOST,
        config.DB_PORT,
        config.DB_USER,
        config.DB_PASSWORD,
        config.DB_NAME,
        config.DB_TABLE,
    )

    # Search
    ret = search.search_vector(query_vector.tolist(), 3)
    print(f"{ret[0]['distance']} : {ret[0]['file_url']}")
    print(f"{ret[1]['distance']} : {ret[1]['file_url']}")
    print(f"{ret[2]['distance']} : {ret[2]['file_url']}")
