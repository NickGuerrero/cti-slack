from datetime import datetime
from logging import Logger
from slack_sdk import WebClient

from api import get_student_info
from listeners.views.home import build_error_home_view, build_home_view
from logs.log_helpers import log_done, log_error, log_trigger_start
from logs.logging_schema import Flow


def render_home_view(
    *,
    client: WebClient,
    user_id: str,
    logger: Logger,
    flow: Flow,
    reason: str,
) -> None:
    """
    Shared renderer: can be called from app_home_opened OR button actions, etc.
    Logs operation-level result (done/error) with duration_ms.
    """

    try:
        # Slack API call(s)
        profile = client.users_profile_get(user=user_id)["profile"]
        user_email = profile.get("email", "")

        # Business data fetch
        student_info = get_student_info(user_email)

        # Handle case where API call succeeded but returned no data
        if not student_info:
            client.views_publish(
                user_id=user_id,
                view=build_error_home_view())
            
            log_error(
                logger=logger,
                flow=flow,
                extra={
                    "operation": "render_home_view",
                    "reason": reason,
                    "result": "no_student_info"
                },
            )
            return

        join_date = (
            datetime.fromisoformat(student_info["join_date"]).strftime("%B %d, %Y")
            if student_info.get("join_date")
            else "N/A"
        )

        client.views_publish(
            user_id=user_id,
            view=build_home_view(
                student_info,
                join_date,
                student_info.get("student_id", "N/A"),
            ),
        )

        log_done(
            logger=logger,
            flow=flow,
            extra={
                "operation": "render_home_view",
                "reason": reason,
            },
        )

    except Exception as e:
        # Publish an error view as a fallback
        try:
            client.views_publish(user_id=user_id, view=build_error_home_view())
        except Exception:
            # Avoid masking original error; optionally log a secondary error
            pass

        log_error(
            logger=logger,
            flow=flow,
            err=e,
            extra={
                "operation": "render_home_view",
                "reason": reason,
            },
        )
        raise

def app_home_opened_callback(client: WebClient, event: dict, logger: Logger) -> None:
    # ignore the app_home_opened event for anything but the Home tab
    if event.get("tab") != "home":
        return
    
    flow = Flow.start(context=event)
    user_id = event.get("user", "unknown")

    log_trigger_start(
        logger=logger,
        flow=flow,
        trigger_type="event",
        trigger_name="app_home_opened",
        user_id=user_id,
    )

    # Call shared renderer
    render_home_view(
        client=client,
        user_id=user_id,
        logger=logger,
        flow=flow,
        reason="app_home_opened",
    )