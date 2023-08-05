from flask import Flask, Blueprint
from slackeventsapi import SlackEventAdapter
import config


blueprint = Blueprint("slack_event_listener", __name__)
slack_events_adapter = SlackEventAdapter(config.SLACK_SIGNING_SECRET, "/slack/events", blueprint)


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
  emoji = event_data["event"]["reaction"]
  print("이모지 달았다")
  print(emoji)


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("message.im")
def on_message(event_data):
  print(event_data)


@slack_events_adapter.on("message")
def handle_message(event_data):
  print(event_data)


@slack_events_adapter.on("message.channels")
def handle_channel_message(event_data):
  print(event_data)