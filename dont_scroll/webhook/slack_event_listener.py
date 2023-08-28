import os

import requests
from flask import Blueprint, Flask
from PIL import Image
from slackeventsapi import SlackEventAdapter

from dont_scroll import config, utils

default = os.path.join(os.path.expanduser("~"), ".config/dont_scroll/config.toml")
config.load(default)

blueprint = Blueprint("slack_event_listener", __name__)
slack_events_adapter = SlackEventAdapter(
    config.SLACK_SIGNING_SECRET, "/slack/events", blueprint
)


@slack_events_adapter.on("message")
def handle_message(event_data):
    event = event_data["event"]

    if "files" in event.keys():
        print(event["text"])
        print(event["user"])
        print(event["channel"])
        print(event["ts"])

        for f in event["files"]:
            id = f["id"]
            fname = f["name"]
            mimetype = f["mimetype"]
            download_url = f["url_private_download"]

            if mimetype.startswith("image"):
                width, height = f["original_w"], f["original_h"]
                img_npy = utils.read_image_from_url(
                    download_url, token=config.BOT_USER_OAUTH_TOKEN
                )
                print(fname, mimetype, download_url, img_npy.shape, width, height)


if __name__ == "__main__":
    config.load("")
    print(config.SLACK_SIGNING_SECRET)
