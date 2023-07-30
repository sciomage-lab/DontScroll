from flask import Flask
from slackeventsapi import SlackEventAdapter


# This `app` represents your existing Flask app
app = Flask(__name__)

# An example of one of your Flask app's routes
@app.route("/")
def hello():
  print("hello")
  return "Hello there!"


# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.

SLACK_SIGNING_SECRET="9e367578fe0fd95c6df91c40bec6e533"
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)


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



# Start the server on port 3000
if __name__ == "__main__":
  app.run(port=3000, debug=True)
