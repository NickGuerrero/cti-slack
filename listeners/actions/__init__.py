from slack_bolt import App

from .home import handle_refresh


def register(app: App):
    app.action("handle_refresh")(handle_refresh)
