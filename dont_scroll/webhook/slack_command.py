# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


import argparse
import os
import math
import time
import datetime

from llama_cpp import Llama
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from dont_scroll import config
from dont_scroll.core.db.search import SearchEngine
from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.core.text_message import TextMessage
from dont_scroll.prompt.prompt_generator import PromptGenerator
from dont_scroll.utils import remove_special_chars_and_spaces

app = None


def read_config():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=os.path.join(
            os.path.expanduser("~"), ".config/dont_scroll/config.toml"
        ),
        type=str,
    )

    args = parser.parse_args()
    config.load(args.config)

    # BOT_USER_OAUTH_TOKEN
    # https://api.slack.com/apps -> DontScroll
    # -> Feature -> OAuth & Permissions
    # -> OAuth Tokens for Your Workspace -> Bot User Oath Token

    # SLACK_APP_TOKEN
    # https://api.slack.com/apps -> DontScroll
    # -> Settings -> Basic Information -> App-Level Tokens
    # -> "TalkTest" -> Token (NEED connetions:write)

    return config


# get config keys
config = read_config()

# ImageRetrieval
image_retrieval = ImageRetrieval()

# SearchEngine
search = SearchEngine(
    config.DB_HOST,
    config.DB_PORT,
    config.DB_USER,
    config.DB_PASSWORD,
    config.DB_NAME,
    config.DB_TABLE,
)

# Text Message
TEXT_MESSAGE = TextMessage()
TEST_MESSAGE = TEXT_MESSAGE.get_all_message()

TEMPLATE = "llama32_ko"

# LLM Model
print("load llama model start...")
llm = Llama(model_path="models/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf", n_ctx=2048)
print("load llama model done.")

# warmup
print("warmup start...")
time_start = time.time()
prompt_generator = PromptGenerator(TEST_MESSAGE, "warmup", template=TEMPLATE)
prompt = str(prompt_generator)
llm(prompt, temperature=0.6)
time_end = time.time()
print(f"warmup : {datetime.timedelta(seconds=(time_end - time_start))}")

# Initializes your app with your bot token and socket mode handler
# get client
if __debug__:
    import ssl

    import certifi

    ssl._create_default_https_context = ssl._create_unverified_context
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # TODO : logger
    print(f"[INFO] XXX : Certificate Verification Disablement!!")
    app = App(client=WebClient(token=config.BOT_USER_OAUTH_TOKEN, ssl=ssl_context))
else:
    app = App(token=config.BOT_USER_OAUTH_TOKEN)


# https://api.slack.com/apps -> DontScroll
# Feature -> Slash Commands -> Crate New Command -> 내부 항목 추가
@app.command("/f")
def handle_find_command(ack, command, respond):
    print("find")
    ack()

    user_id = command["user_id"]
    text = command["text"]

    query = text
    query_vector = image_retrieval.text_to_vector(query)

    ret = search.search_vector(query_vector.tolist(), 3)
    print(ret[0]["file_url"])
    print(ret[1]["file_url"])

    response_text = f"""
    To <@{user_id}> : {text} search 
    - {ret[0]['distance']} : {ret[0]['file_url']} 
    - {ret[1]['distance']} : {ret[1]['file_url']}"""
    respond(response_text)


# https://api.slack.com/apps -> DontScroll
# Feature -> Slash Commands -> Crate New Command -> 내부 항목 추가
@app.command("/q")
def handle_query_command(ack, command, respond):
    ack()

    user_id = command["user_id"]
    query = command["text"]

    prompt_generator = PromptGenerator(TEST_MESSAGE, query, template=TEMPLATE)
    prompt = str(prompt_generator)

    print(f"prompt : {prompt}")

    output = llm(prompt, temperature=0.1)
    print(output)
    print("===== RESULT =====")
    result = remove_special_chars_and_spaces(output["choices"][0]["text"])
    print(result)

    response_text = f"""
    To <@{user_id}> : {query} : 
    `{result}`"""
    respond(response_text)


if __name__ == "__main__":
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()
