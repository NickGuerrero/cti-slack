import os
from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

load_dotenv() # In Heroku, make sure values are set in config vars

# Use bot token + socket handler
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Respond to hello message
@slack_app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# Flask Handler Set-Up
flask_app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Conditional launcher
if __name__ == "__main__" and os.environ.get("SLACK_APP_TOKEN"):
    # Development: Use SocketMode
    SocketModeHandler(slack_app, os.environ.get("SLACK_APP_TOKEN")).start()

