from slack_bolt import Say


def message_hello_callback(event, say: Say):
    # say() sends a message to the channel where the event was triggered
    if event.get("text", "").lower() == "hello":
        say(f"Hey there <@{event['user']}>!")
        