import requests

from config import Config

def get_student_info(user_email: str) -> dict:
    headers = {
        "Authorization": f"Bearer {Config.cti_sys_api_key}"
    }

    response = requests.get(
        url=f"{Config.cti_sys_url}/api/slack/students/info?user_email={user_email}",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()
