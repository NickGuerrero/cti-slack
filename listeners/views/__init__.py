from slack_bolt import App


def register(app: App):
    from listeners.actions.email_form import handle_email_form_submit

    app.view("email_form_modal")(handle_email_form_submit)
