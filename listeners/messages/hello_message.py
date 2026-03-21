from slack_bolt import Say


def message_hello_callback(event, say: Say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{event['user']}>!")
        