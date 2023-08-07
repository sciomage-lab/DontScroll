import numpy as np

from dont_scroll.core.db.postgresql import PostgreSQLClient
from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.core.utils import cos_sim

# TODO : Select DB
DB_CLIENT = PostgreSQLClient

# TODO : config file
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "dont_scroll"
DB_PASSWORD = "passwd"
DB_NAME = "dont_scroll_db"
DB_TABLE = "public.slack_message"


class SearchEngine:
    def __init__(self, host, port, user, password, db_name, db_table):
        self.db_client = DB_CLIENT(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
            db_table=db_table,
        )

        if self.db_client.connection == None:
            # TODO: logger
            print("DB connect fail")

    def add_vector(self, vector: list, url: str):
        """Add vector
        :param list vector: input vector
        :param str url: input url
        """
        data = {
            "vector": f"CUBE(ARRAY[{vector}])",
            "url": url,
        }
        self.db_client.insert_data(data)

    def search_vector(self, vector: list, n: int):
        """
        Search vector
        :param list vector : vector
        :param n int : top-n
        """
        ret = self.db_client.select_vector(vector, n)
        return ret


if __name__ == "__main__":
    image_path_1 = "./tests/images/cat1.png"
    image_path_2 = "./tests/images/cat2.jpg"
    image_path_3 = "./tests/images/hedgehog1.jpg"
    image_path_4 = "./tests/images/hedgehog2.jpg"
    image_retrieval = ImageRetrieval()
    image_vector_1 = image_retrieval.image_to_vector(image_path_1)
    image_vector_2 = image_retrieval.image_to_vector(image_path_2)
    image_vector_3 = image_retrieval.image_to_vector(image_path_3)
    image_vector_4 = image_retrieval.image_to_vector(image_path_4)
    print(f"cat1 vector shaep : {image_vector_1.shape}")
    print(f"cat2 vector shape : {image_vector_2.shape}")
    print(f"hedgehog1 vector shape : {image_vector_3.shape}")
    print(f"hedgehog2 vector shape : {image_vector_4.shape}")

    text_vector = image_retrieval.text_to_vector("hedgehog")
    print(f"text vector shape : {text_vector.shape}")

    # TODO : configfile
    search = SearchEngine(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_TABLE)

    # Add
    search.add_vector(image_vector_1.tolist(), image_path_1)
    search.add_vector(image_vector_3.tolist(), image_path_3)
    search.add_vector(image_vector_4.tolist(), image_path_4)

    # Search : Image
    ret = search.search_vector(image_vector_2.tolist(), 3)
    print("Image search")
    print(ret[0]["url"])
    print(ret[1]["url"])
    print(ret[2]["url"])

    # Search : Text
    print("Text search")
    ret = search.search_vector(text_vector.tolist(), 3)
    print(ret[0]["url"])
    print(ret[1]["url"])
    print(ret[2]["url"])

    # Delete
    search.db_client.delete_data("url", [image_path_1, image_path_3, image_path_4])
