from slack_sdk import WebClient
import requests
import json
import os
import re

# auth
# auth token - https://api.slack.com/apps
# 1, url에서 앱을 만들고
# 2, 좌측 OAuth & Permission에 들어가서
# 3, Scopes 추가, "app_mentions:read, channels:history"는 기본으로 추가하고 필요하면 더 추가
auth_token = "xoxb-5683781764640-5663727658034-Umgt4L0BXVAlbJlsziXFROa0"

# channel id - https://api.slack.com/methods/conversations.list/test
# 1, url들아가면 tester페이지가 나옴
# 2, 위의 auth_token을 집어 넣고 "Test method" 녹색 버튼 누르면
# 3, json으로 간단한 정보가 뜨는데 거기서 channel->id를 보면 채팅방에 따른 id가 뜬다.
# 4, 그중에서 적절한것을 하나 골라서 channel_id로 사용하면 됨
# channel_id = "C05KGFK5D1S" # OSS
channel_id = "C05L7M02A80" # LogTest

# 이제 채널에 봇을 초대하고, 아래 코드를 실행하면 txt파일이 출력됨

def parsing(client):
    response = client.conversations_history(channel=channel_id)

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
        image_response = requests.get(image_url, headers={"Authorization": f"Bearer {auth_token}"})
        save_filename = os.path.basename(image_url)
        
        with open(save_filename, "wb") as image_file:
            image_file.write(image_response.content)
        
def getLink(message_list):
    urls = []
    url_pattern = re.compile(r'https?://\S+')

    for message in message_list:
        urls.extend(re.findall(url_pattern, message))

    return urls

# Slack API
client = WebClient(token=auth_token)

# Load message
text_list, image_url_list = parsing(client)

# Save file
saveLog("chat.log", text_list)
saveImage(image_url_list, auth_token)

# get Link
message_link = getLink(text_list)
print(message_link)
