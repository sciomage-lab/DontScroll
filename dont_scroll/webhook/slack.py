import argparse
import json
import os
import re
import requests

from slack_sdk import WebClient

from dont_scroll.core.db.search import SearchEngine
from dont_scroll import config
from dont_scroll.utils import set_timescope
from dont_scroll.logger import applogger


class SlackMessageFetcher:
    def __init__(self, auth_token: str, channel_id: str):
        # auth
        # auth token - https://api.slack.com/apps
        # 1, url에서 앱을 만들고
        # 2, 좌측 OAuth & Permission에 들어가서
        # 3, Scopes 추가, "app_mentions:read, channels:history"는 기본으로 추가하고 필요하면 더 추가
        if auth_token == None or auth_token == "":
            applogger.critical(f"Error auth_token is invalid")
            exit()

        # channel id - https://api.slack.com/methods/conversations.list/test
        # 1, url들아가면 tester페이지가 나옴
        # 2, 위의 auth_token을 집어 넣고 "Test method" 녹색 버튼 누르면
        # 3, json으로 간단한 정보가 뜨는데 거기서 channel->id를 보면 채팅방에 따른 id가 뜬다.
        # 4, 그중에서 적절한것을 하나 골라서 channel_id로 사용하면 됨
        if channel_id == None or channel_id == "":
            applogger.critical(f"Error auth_token is invalid")
            exit()

        self.auth_token = auth_token
        self.channel_id = channel_id

        # get client
        if __debug__:
            import ssl
            import certifi

            ssl._create_default_https_context = ssl._create_unverified_context
            ssl_context = ssl.create_default_context(cafile=certifi.where())

            # TODO : logger
            applogger.debug(f"[INFO] XXX : Certificate Verification Disablement!!")
            self.client = WebClient(token=auth_token, ssl=ssl_context)
        else:
            self.client = WebClient(token=auth_token)

    def get_response(self):
        return self.client.conversations_history(channel=self.channel_id)

    def get_response(self, oldest_timestamp, latest_timestamp):
        return self.client.conversations_history(
            channel=self.channel_id, oldest=oldest_timestamp, latest=latest_timestamp
        )

    def get_text_image(self, oldest_timestamp, latest_timestamp):
        response = self.get_response(oldest_timestamp, latest_timestamp)

        ret = []
        if response["ok"]:
            messages = response["messages"]

            for message in messages:
                # print(f"message : {message}")
                # message
                if (
                    "text" in message
                    and "files" in message
                    and "client_msg_id" in message
                ):
                    text = message["text"] or "(empty)"
                    files = message["files"]
                    client_msg_id = message["client_msg_id"]

                    # images
                    for file in files:
                        file_url = file["url_private"]

                        print(f"[{client_msg_id}] {text} : {file_url[:100]}")
                        ret.append(
                            {
                                "client_msg_id": client_msg_id,
                                "text": text,
                                "file_url": file_url,
                            }
                        )
        return ret


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


def saveLog(filename, text_list):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(text_list))


def saveImage(image_url_list, auth_token):
    for image_url in image_url_list:
        image_response = requests.get(
            image_url, headers={"Authorization": f"Bearer {auth_token}"}
        )
        save_filename = os.path.basename(image_url)

        with open(save_filename, "wb") as image_file:
            image_file.write(image_response.content)


def getLink(message_list):
    urls = []
    url_pattern = re.compile(r"https?://\S+")

    for message in message_list:
        urls.extend(re.findall(url_pattern, message))

    return urls


# module test
if __name__ == "__main__":
    toml = read_config()
    auth_token = toml.BOT_USER_OAUTH_TOKEN
    channel_id = toml.CHANNEL_ID

    slack_message_fetcher = SlackMessageFetcher(auth_token, channel_id)

    # set tiemstamp
    start_datetime, end_datetime = set_timescope(2023, 7, 1, 0, 0, 0, 60, 0, 0, 0)

    # Load message
    response_data = slack_message_fetcher.get_response(start_datetime, end_datetime)

    search = SearchEngine(
        config.DB_HOST,
        config.DB_PORT,
        config.DB_USER,
        config.DB_PASSWORD,
        config.DB_NAME,
        config.DB_TABLE,
    )

    # Parsing
    message_list = slack_message_fetcher.get_text_image(
        start_datetime, end_datetime
    )

    print(json.dumps(message_list, indent=4, ensure_ascii=False))

    # Save messages
    # saveLog("chat.log", text_list)

    # Save attached images
    # saveImage(image_url_list, auth_token)

    # get URL Link
    # message_link = getLink(text_list)
