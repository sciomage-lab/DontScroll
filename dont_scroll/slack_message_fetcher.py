import argparse
import json
import os
import re
import time
from io import BytesIO

import requests
from PIL import Image, UnidentifiedImageError

# For test
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from slack_sdk import WebClient

from dont_scroll import config
from dont_scroll.core.db.search import SearchEngine
from dont_scroll.core.image_retrieval import ImageRetrieval
from dont_scroll.logger import applogger
from dont_scroll.utils import is_image_file, set_timescope, timestamp_to_str, unix_timestamp_to_datetime


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
        applogger.debug(f"auth_token : {auth_token}")
        applogger.debug(f"channel_id : {channel_id}")

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

    def get_all_messages(self):
        """Get all message"""
        return self.client.conversations_history(channel=self.channel_id)

    def get_all_messages(self, oldest_timestamp, latest_timestamp):
        """Get all message
        :param oldest_timestamp:
        :param latest_timestamp:
        """
        return self.client.conversations_history(
            channel=self.channel_id, oldest=oldest_timestamp, latest=latest_timestamp
        )

    def get_messages(self, oldest_timestamp, latest_timestamp):
        """Get messages (text & image)"""

        # Get all message
        response = self.get_all_messages(oldest_timestamp, latest_timestamp)

        ret = []
        if response["ok"]:
            messages = response["messages"]
        else:
            # Fail
            return ret

        # Parsing message
        for message in messages:
            # Debug
            # print(f"message : {message}")

            if "text" in message and "client_msg_id" in message:
                text = message["text"] or "(empty)"
                client_msg_id = message["client_msg_id"]
                ts = float(message["ts"])

                # Exist files
                if "files" in message:
                    # Exist files
                    files = message["files"]

                    # Loop : image files
                    for file in files:
                        file_url = file["url_private"]
                        file_id = file["id"]

                        print(f"[{client_msg_id}] : {ts} : {timestamp_to_str(ts)} : {text} : {file_url[:100]}")
                        ret.append(
                            {
                                "client_msg_id": f"{client_msg_id}-{file_id}",
                                "text": text,
                                "file_url": file_url,
                                "ts": ts,
                            }
                        )
                else:
                    # No Exist files
                    print(f"[{client_msg_id}] : {ts} : {timestamp_to_str(ts)}: {text}")
                    ret.append(
                        {
                            "client_msg_id": f"{client_msg_id}",
                            "text": text,
                            "file_url": None,
                            "ts": ts,
                        }
                    )

        return ret

    def get_image(self, image_url):
        """Get image file"""

        if is_image_file(image_url) is False:
            return None

        response = requests.get(
            image_url, headers={"Authorization": f"Bearer {self.auth_token}"}
        )

        if response.status_code == 200:  # HTTP 상태 코드가 200 OK인 경우
            try:
                img_data = BytesIO(response.content)
                img_data.seek(0)
                img = Image.open(img_data)
            except UnidentifiedImageError:
                # TODO : error
                print("Cannot identify image file")
                return None
        else:
            print("Error, image get error")
            pass

        return img


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
    config = read_config()
    auth_token = config.BOT_USER_OAUTH_TOKEN
    channel_id = config.CHANNEL_ID

    slack_message_fetcher = SlackMessageFetcher(auth_token, channel_id)

    # set tiemstamp
    # TODO :
    start_datetime, end_datetime = set_timescope(2023, 9, 1, 0, 0, 0, 90, 0, 0, 0)

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

    # Parsing
    message_list = slack_message_fetcher.get_messages(start_datetime, end_datetime)
    # DEBUG
    # print(json.dumps(message_list, indent=4, ensure_ascii=False))

    # Progress
    client_msg_id = ""
    with Progress() as progress:
        task = progress.add_task("[insert DB]", total=len(message_list))

        for message in message_list:
            client_msg_id = message["client_msg_id"]
            text = message["text"]
            ts = message["ts"]
            file_url = message["file_url"]

            is_exist = search.exist_msg_id(client_msg_id)
            if is_exist:
                # already exists (duplicate)
                continue 
            elif file_url is not None:
                # Exist file url
            
                # Get image
                image_buf = slack_message_fetcher.get_image(file_url)
                if image_buf is None:
                    continue

                # To vector
                vector = image_retrieval.image_to_vector(image_buf).tolist()

                # Insert DB
                ts_datetime = unix_timestamp_to_datetime(ts)
                search.add_vector(vector, file_url, client_msg_id, text, ts_datetime)
            else:
                # No exist file url

                # Insert DB
                ts_datetime = unix_timestamp_to_datetime(ts)
                search.add_message(client_msg_id, text, ts_datetime)

            progress.advance(task)

    # Save messages
    # saveLog("chat.log", text_list)

    # Save attached images
    # saveImage(image_url_list, auth_token)

    # get URL Link
    # message_link = getLink(text_list)

    # TEST
    # TODO :
    query = "hedgehog"
    query_vector = image_retrieval.text_to_vector(query)

    ret = search.search_vector(query_vector.tolist(), 3)
    print(ret[0]["file_url"])
    print(ret[1]["file_url"])
    print(ret[2]["file_url"])
