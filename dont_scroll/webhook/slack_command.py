import argparse
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from dont_scroll import config


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


# get toml keys
toml = read_config()

# Initializes your app with your bot token and socket mode handler
# get client
if __debug__:
    import ssl

    import certifi

    ssl._create_default_https_context = ssl._create_unverified_context
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # TODO : logger
    print(f"[INFO] XXX : Certificate Verification Disablement!!")
    app = App(client=WebClient(token=toml.BOT_USER_OAUTH_TOKEN, ssl=ssl_context))
else:
    app = App(token=toml.BOT_USER_OAUTH_TOKEN)


# https://api.slack.com/apps -> DontScroll
# Feature -> Slash Commands -> Crate New Command -> 내부 항목 추가
@app.command("/welcome")
def handle_welcome_command(ack, command, respond):
    ack()

    user_id = command["user_id"]
    need_drink = command["text"]
    response_text = f"To <@{user_id}> : Welcome drink here! {need_drink}"

    respond(response_text)


if __name__ == "__main__":
    SocketModeHandler(app, toml.SLACK_APP_TOKEN).start()
