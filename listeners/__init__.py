from slack_bolt import App

from listeners import events, messages, actions

def register_listeners(app: App):
    events.register(app)
    messages.register(app)
    actions.register(app)
