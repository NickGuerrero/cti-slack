import time

from logging import Logger
from slack_sdk.web.client import WebClient
from slack_bolt import Ack

from listeners.events.app_home_opened import render_home_view
from logs.log_helpers import log_trigger_start
from logs.logging_schema import Flow

def handle_refresh(ack: Ack, body: dict, client: WebClient, logger: Logger):
    flow = Flow.start(body=body)
    user_id = body.get("user", {}).get("id", "unknown")

    log_trigger_start(
        logger=logger,
        flow=flow,
        trigger_type="action",
        trigger_name="home_refresh_button",
        user_id=user_id,
    )

    ack_start_ms = int(time.time() * 1000)
    ack()
    flow.mark_acked(ack_start_ms=ack_start_ms)

    render_home_view(
        client=client,
        user_id=user_id,
        logger=logger,
        flow=flow,
        reason="home_refresh_button",
    )
