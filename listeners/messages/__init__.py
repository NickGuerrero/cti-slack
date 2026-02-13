from slack_bolt import App
from .hello_message import message_hello_callback


def register(app: App):
    app.event("message")(message_hello_callback)
