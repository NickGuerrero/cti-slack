from slack_bolt import App

from .home import handle_refresh
from .email_form import handle_update_emails, handle_delete_email, handle_add_email


def register(app: App):
    app.action("handle_refresh")(handle_refresh)
    app.action("update_emails")(handle_update_emails)
    app.action("delete_email")(handle_delete_email)
    app.action("add_email")(handle_add_email)
