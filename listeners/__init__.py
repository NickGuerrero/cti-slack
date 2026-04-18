from slack_bolt import App

from listeners import events, messages, actions, views

def register_listeners(app: App):
    events.register(app)
    messages.register(app)
    actions.register(app)
    views.register(app)
