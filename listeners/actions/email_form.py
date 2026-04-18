import json
import time

from logging import Logger
from slack_sdk.web.client import WebClient
from slack_bolt import Ack

from api import get_student_info
from listeners.views.email_form import build_email_form_view
from logs.log_helpers import log_trigger_start, log_done, log_error
from logs.logging_schema import Flow


def handle_update_emails(ack: Ack, body: dict, client: WebClient, logger: Logger):
    flow = Flow.start(body=body)
    user_id = body.get("user", {}).get("id", "unknown")

    log_trigger_start(
        logger=logger,
        flow=flow,
        trigger_type="action",
        trigger_name="update_emails",
        user_id=user_id,
    )

    ack_start_ms = int(time.time() * 1000)
    ack()
    flow.mark_acked(ack_start_ms=ack_start_ms)

    try:
        profile = client.users_profile_get(user=user_id)["profile"]
        user_email = profile.get("email", "")
        student_info = get_student_info(user_email)

        primary_email = student_info.get("primary_email", user_email)
        alternate_emails = student_info.get("alternate_emails", []) if student_info.get("alternate_emails") else []

        client.views_open(
            trigger_id=body["trigger_id"],
            view=build_email_form_view(primary_email, alternate_emails),
        )

        log_done(
            logger=logger,
            flow=flow,
            extra={"operation": "open_email_form"},
        )

    except Exception as e:
        log_error(
            logger=logger,
            flow=flow,
            err=e,
            extra={"operation": "open_email_form"},
        )
        raise


def handle_delete_email(ack: Ack, body: dict, client: WebClient, logger: Logger):
    flow = Flow.start(body=body)

    ack_start_ms = int(time.time() * 1000)
    ack()
    flow.mark_acked(ack_start_ms=ack_start_ms)

    metadata = json.loads(body["view"]["private_metadata"])
    email_to_remove = body["actions"][0]["value"]

    alternate_emails = [e for e in metadata["alternate_emails"] if e != email_to_remove]

    client.views_update(
        view_id=body["view"]["id"],
        view=build_email_form_view(metadata["primary_email"], alternate_emails),
    )


def handle_add_email(ack: Ack, body: dict, client: WebClient, logger: Logger):
    flow = Flow.start(body=body)

    ack_start_ms = int(time.time() * 1000)
    ack()
    flow.mark_acked(ack_start_ms=ack_start_ms)

    metadata = json.loads(body["view"]["private_metadata"])
    state_values = body["view"]["state"]["values"]
    new_email = (
        state_values
        .get("email_input_block", {})
        .get("email_input_value", {})
        .get("value")
    )

    alternate_emails = metadata["alternate_emails"]
    if new_email and new_email not in alternate_emails and new_email != metadata["primary_email"]:
        alternate_emails.append(new_email)

    client.views_update(
        view_id=body["view"]["id"],
        view=build_email_form_view(metadata["primary_email"], alternate_emails),
    )


def handle_email_form_submit(ack: Ack, body: dict, client: WebClient, view: dict, logger: Logger):
    flow = Flow.start(body=body)
    user_id = body.get("user", {}).get("id", "unknown")

    log_trigger_start(
        logger=logger,
        flow=flow,
        trigger_type="view_submission",
        trigger_name="email_form_modal",
        user_id=user_id,
    )

    ack_start_ms = int(time.time() * 1000)
    ack()
    flow.mark_acked(ack_start_ms=ack_start_ms)

    metadata = json.loads(view["private_metadata"])

    try:
        # TODO: replace with real backend call, e.g.
        # requests.put(f"{Config.cti_sys_url}/api/slack/students/emails", json=metadata, headers=...)
        logger.info({
            "operation": "mock_update_emails",
            "primary_email": metadata["primary_email"],
            "alternate_emails": metadata["alternate_emails"],
        })

        client.chat_postMessage(
            channel=user_id,
            text=":white_check_mark: Your emails have been updated successfully.",
        )

        log_done(
            logger=logger,
            flow=flow,
            extra={"operation": "email_form_submit"},
        )

    except Exception as e:
        client.chat_postMessage(
            channel=user_id,
            text=":warning: Something went wrong updating your emails. Please try again later.",
        )

        log_error(
            logger=logger,
            flow=flow,
            err=e,
            extra={"operation": "email_form_submit"},
        )
