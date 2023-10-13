import os

import pytest

from dont_scroll import config
from dont_scroll.core.db.search import SearchEngine
from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.utils import generate_random_hash


class TextMessage:
    def __init__(self, config_path: str = None):
        if config_path == None:
            config_path = os.path.join(
                os.path.expanduser("~"), ".config/dont_scroll/config.toml"
            )

        config.load(config_path)

        self.search = SearchEngine(
            config.DB_HOST,
            config.DB_PORT,
            config.DB_USER,
            config.DB_PASSWORD,
            config.DB_NAME,
            config.DB_TABLE,
        )

    def get_all_message(self, top_n: int = 1000):
        messages = self.search.top_n_msg(100)

        text = ""
        for message in messages:
            text += f"{message['user_id']} : {message['text']}\n"

        return text


if __name__ == "__main__":
    text_message = TextMessage()
    result = text_message.get_all_message()

    print(f"{result}")
