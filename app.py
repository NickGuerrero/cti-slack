import logging
import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from slack_sdk import WebClient

load_dotenv() # In Heroku, make sure values are set in config vars

SYS_URL = os.environ.get("CTI_SYS_URL")
API_KEY = os.environ.get("CTI_SYS_API_KEY")
SIGNING_SECRET=os.environ.get("SLACK_SIGNING_SECRET")
BOT_TOKEN=os.environ.get("SLACK_BOT_TOKEN")
APP_TOKEN=os.environ.get("SLACK_APP_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Use bot token + socket handler
slack_app = App(
    token=BOT_TOKEN,
    signing_secret=SIGNING_SECRET
)

@slack_app.event("app_home_opened")
def update_home_tab(client: WebClient, event, logger: logging.Logger):
    start = time.time()
    user_id = event["user"]
    user_email = client.users_profile_get(user=user_id)["profile"].get("email", "")
    try:        
        # Fetch user information from cti-sys
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        response = requests.get(
            url=f"{SYS_URL}/api/slack/students/info?user_email={user_email}",
            headers=headers,
        )

        # print(response.status_code, response.json())
        student_info = response.json()

        join_date = datetime.fromisoformat(
            student_info['join_date']
        ).strftime("%B %d, %Y") if student_info.get('join_date') else "N/A"

        # Call views.publish with the built-in client
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": [

                    # Student Information Section
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*CTI Student:* {student_info['fname']} {'\'' + student_info['pname'] + '\'' if student_info['pname'] else ''} {student_info['lname']}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Target Year:* {student_info['target_year']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Join Date:* {join_date}"
                            }
                        ]
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "View Student Information"
                                },
                                "action_id": "view_student_info",
                                "value": "STUDENT_ID"
                            }
                        ]
                    },
                    {"type": "divider"},

                    # Emails Section
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Registered Emails*\n\n*Primary Email:* guerreronicolas1872@gmail.com\n*Alternative Emails:* nicolas.guerrero@sjsu.edu, nicguerrero@csumb.edu"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Update Emails"
                                },
                                "action_id": "update_emails",
                                "value": "STUDENT_ID"
                            }
                        ]
                    },
                    {"type": "divider"},

                    # Attendance Section
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Attendance*\nSessions attended this year: *20*\n*Last Sessions Attended*\n• October 31, 2025 (40% Interactions)\n• November 6, 2025 (80% Interactions)\n• November 14, 2025 (60% Interactions)"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "See Attendance History"
                                },
                                "action_id": "see_attendance_history",
                                "value": "STUDENT_ID"
                            }
                        ]
                    },
                    {"type": "divider"},

                    # Badges Section
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Badge Progress* _(TODO: ignore for now)_"
                        }
                    },
                    {
                        "type": "image",
                        "image_url": "https://picsum.photos/200",
                        "alt_text": "Badge progress row"
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "See Badges"
                                },
                                "action_id": "see_badges",
                                "value": "STUDENT_ID"
                            }
                        ]
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@slack_app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# Flask Handler Set-Up
flask_app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Conditional launcher
if __name__ == "__main__" and APP_TOKEN:
    # Development: Use SocketMode
    SocketModeHandler(slack_app, APP_TOKEN).start()

