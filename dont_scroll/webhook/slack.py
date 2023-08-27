import datetime
import json
import os
import re

import requests
from slack_sdk import WebClient

# auth
# auth token - https://api.slack.com/apps
# 1, url에서 앱을 만들고
# 2, 좌측 OAuth & Permission에 들어가서
# 3, Scopes 추가, "app_mentions:read, channels:history"는 기본으로 추가하고 필요하면 더 추가

# TODO : Load config
auth_token = os.environ.get("auth_token")
if auth_token == None or auth_token == "":
    # TODO : Error
    print(f"Error auth_token is invalid")
    exit()

# channel id - https://api.slack.com/methods/conversations.list/test
# 1, url들아가면 tester페이지가 나옴
# 2, 위의 auth_token을 집어 넣고 "Test method" 녹색 버튼 누르면
# 3, json으로 간단한 정보가 뜨는데 거기서 channel->id를 보면 채팅방에 따른 id가 뜬다.
# 4, 그중에서 적절한것을 하나 골라서 channel_id로 사용하면 됨

# TODO : Load config
channel_id = os.environ.get("channel_id")
if channel_id == None or channel_id == "":
    # TODO : Error
    print(f"Error auth_token is invalid")
    exit()


# 이제 채널에 봇을 초대하고, 아래 코드를 실행하면 txt파일이 출력됨


def set_timescope(
    start_year,
    start_month,
    start_day,
    start_hour,
    start_minute,
    start_second,
    add_day,
    add_hour,
    add_minute,
    add_second,
):
    start_date = datetime.datetime(
        start_year, start_month, start_day, start_hour, start_minute, start_second
    )
    datetime_scope = datetime.timedelta(
        days=add_day, hours=add_hour, minutes=add_minute, seconds=add_second
    )

    return int(start_date.timestamp()), int((start_date + datetime_scope).timestamp())


def get_response(client):
    return client.conversations_history(channel=channel_id)


def get_response(client, oldest_timestamp, latest_timestamp):
    return client.conversations_history(
        channel=channel_id, oldest=oldest_timestamp, latest=latest_timestamp
    )


def get_text_image(response):
    if response["ok"]:
        messages = response["messages"]
        text_list = []
        image_list = []

        for message in messages:
            # message
            if "text" in message:
                text_list.append(message["text"])

            # files
            if "files" in message:
                files = message["files"]

                # images
                for file in files:
                    image_list.append(file["url_private"])

    return text_list, image_list


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


# get client
if __debug__:
    import certifi
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # TODO : logger
    print(f"[INFO] XXX : Certificate Verification Disablement!!")
    client = WebClient(token=auth_token, ssl=ssl_context)
else:
    client = WebClient(token=auth_token)

# set tiemstamp
start_datetime, end_datetime = set_timescope(2023, 7, 1, 0, 0, 0, 60, 0, 0, 0)

# Load message
response_data = get_response(client, start_datetime, end_datetime)

# print(json.dumps(response_data['messages'], indent=4, ensure_ascii=False))

# Parsing
text_list, image_url_list = get_text_image(response_data)

# Save messages
saveLog("chat.log", text_list)

# Save attached images
saveImage(image_url_list, auth_token)

# get URL Link
message_link = getLink(text_list)
