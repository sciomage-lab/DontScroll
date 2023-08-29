import argparse
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from dont_scroll import config
from dont_scroll.core.db.search import SearchEngine
from dont_scroll.core.image_retrieval import ImageRetrieval

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
@app.command("/find")
def handle_welcome_command(ack, command, respond):
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
    - {ret[0]['file_url']} 
    - {ret[1]['file_url']}"""
    respond(response_text)


if __name__ == "__main__":
    SocketModeHandler(app, config.SLACK_APP_TOKEN).start()
