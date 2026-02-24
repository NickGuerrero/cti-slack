from logging import Logger
from slack_sdk.web.client import WebClient
from slack_bolt import Ack

from listeners.events.app_home_opened import app_home_opened_callback 


def handle_refresh(ack: Ack, body: dict, client: WebClient, logger: Logger):
    ack()
    try:
        # Add 'event' values required for app_home_opened_callback
        user_email = body.get("user", {}).get("id", None)
        if user_email is None:
            raise ValueError("User ID not found in action body")
        body['event'] = { "tab": "home", "user": user_email }
        
        app_home_opened_callback(client, body["event"], logger)
        logger.info({"service": "Bolt", "action": "home_refresh"})
    except Exception as e:
        logger.error({"service": "Bolt", "action": "home_refresh_error", "error": str(e)})
