import os

from dotenv import load_dotenv


load_dotenv()

class Config():
    # CTI System Config
    cti_sys_url = os.environ.get("CTI_SYS_URL")
    cti_sys_api_key = os.environ.get("CTI_SYS_API_KEY")

    # Slack App Config
    slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_app_token = os.environ.get("SLACK_APP_TOKEN")
