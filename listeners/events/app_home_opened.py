from datetime import datetime
from logging import Logger
import time
from slack_sdk import WebClient

from api import get_student_info
from listeners.views.home import build_error_home_view, build_home_view


def app_home_opened_callback(client: WebClient, event: dict, logger: Logger):
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    start = time.time()

    user_id = event["user"]
    user_email = client.users_profile_get(user=user_id)["profile"].get("email", "")

    error_occurred = False
    student_info = None
    try:
        student_info = get_student_info(user_email)
    except Exception as e:
        error_occurred = True
        logger.error({"service": "Bolt", "event": "app_home_opened", "status": "error", "error": str(e), "latency_ms": int((time.time()-start)*1000)})

    if error_occurred or not student_info:
        client.views_publish(
            user_id=user_id,
            view=build_error_home_view()
        )
    else:
        join_date = datetime.fromisoformat(
            student_info['join_date']
        ).strftime("%B %d, %Y") if student_info.get('join_date') else "N/A"

        client.views_publish(
            user_id=user_id,
            view=build_home_view(student_info, join_date, student_info.get("student_id", "N/A"))
        )
        logger.info({"service": "Bolt", "event": "app_home_opened", "status": "ok", "latency_ms": int((time.time()-start)*1000)})
