import json

from typing import List

from slack_sdk.models.views import View
from slack_sdk.models.blocks import (
    Block,
    HeaderBlock,
    SectionBlock,
    DividerBlock,
    ActionsBlock,
    InputBlock,
)
from slack_sdk.models.blocks.basic_components import MarkdownTextObject, PlainTextObject
from slack_sdk.models.blocks.block_elements import ButtonElement, EmailInputElement


def build_email_form_view(primary_email: str, alternate_emails: List[str]) -> View:
    private_metadata = json.dumps({
        "primary_email": primary_email,
        "alternate_emails": alternate_emails,
    })

    blocks: List[Block] = [
        HeaderBlock(text=PlainTextObject(text="Update Emails")),

        SectionBlock(
            fields=[
                MarkdownTextObject(text=f"`{primary_email}`"),
                MarkdownTextObject(text="_Primary_"),
            ]
        ),
    ]

    for email in alternate_emails:
        blocks.append(
            SectionBlock(
                text=MarkdownTextObject(text=f"`{email}`"),
                accessory=ButtonElement(
                    text=PlainTextObject(text="Delete"),
                    action_id="delete_email",
                    value=email,
                ),
            )
        )

    blocks.append(DividerBlock())

    blocks.append(
        InputBlock(
            block_id="email_input_block",
            label=PlainTextObject(text="Add a new email"),
            element=EmailInputElement(
                action_id="email_input_value",
                placeholder=PlainTextObject(text="name@example.com"),
            ),
            optional=True,
        )
    )

    blocks.append(
        ActionsBlock(
            elements=[
                ButtonElement(
                    text=PlainTextObject(text="Add"),
                    action_id="add_email",
                ),
            ]
        )
    )

    return View(
        type="modal",
        callback_id="email_form_modal",
        title=PlainTextObject(text="Update Emails"),
        submit=PlainTextObject(text="Update"),
        close=PlainTextObject(text="Close"),
        private_metadata=private_metadata,
        blocks=blocks,
    )
