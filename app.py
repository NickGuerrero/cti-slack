import logging

from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler

from config import Config
from listeners import register_listeners
from logs.logger import init_logger


init_logger(logging.getLogger())

# Use bot token + socket handler
slack_app = App(
    token=Config.slack_bot_token,
    signing_secret=Config.slack_signing_secret
)

register_listeners(slack_app)

# Flask Handler Set-Up
flask_app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("slack/interactions", methods=["POST"])
def slack_interactions():
    return handler.handle(request)

# Conditional launcher
if __name__ == "__main__" and Config.slack_app_token:
    # Development: Use SocketMode
    SocketModeHandler(slack_app, Config.slack_app_token).start()

