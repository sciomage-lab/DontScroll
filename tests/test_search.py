import pytest

from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.core.db.search import SearchEngine


# TODO : config file
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "dont_scroll"
DB_PASSWORD = "passwd"
DB_NAME = "dont_scroll_db"
DB_TABLE = "public.slack_message"


@pytest.mark.skip_docker
@pytest.mark.parametrize(
    "data_1, data_2, data_3, query, gt",
    [("cat1.png", "cat2.jpg", "hedgehog1.jpg", "hedgehog2.jpg", "hedgehog1.jpg"),
     ("cat1.png", "cat2.jpg", "hedgehog2.jpg", "hedgehog1.jpg", "hedgehog2.jpg"),
     ("hedgehog1.jpg", "hedgehog2.jpg", "cat1.png", "cat2.jpg", "cat1.png"),
     ("hedgehog1.jpg", "hedgehog2.jpg", "cat2.jpg", "cat1.png", "cat2.jpg")])
def test_search(data_1, data_2, data_3, query, gt):
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

    # TODO : configfile
    search = SearchEngine(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_TABLE)

    # Add
    search.add_vector(data_vector_1.tolist(), data_path_1)
    search.add_vector(data_vector_2.tolist(), data_path_2)
    search.add_vector(data_vector_3.tolist(), data_path_3)

    # Search
    ret = search.search_vector(query_vector.tolist(), 3)
    print(ret[0]["url"])
    print(ret[1]["url"])
    print(ret[2]["url"])

    assert ret[0]["url"] != gt

    # Delete
    search.db_client.delete_data("url", [data_path_1, data_path_2, data_path_3])
