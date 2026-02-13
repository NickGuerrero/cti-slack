from slack_bolt import App

from listeners import events, messages

def register_listeners(app: App):
    events.register(app)
    messages.register(app)
