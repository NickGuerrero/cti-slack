from typing import List

from slack_sdk.models.views import View
from slack_sdk.models.blocks import (
    Block,
    SectionBlock,
    DividerBlock,
    ActionsBlock,
    ImageBlock,
)
from slack_sdk.models.blocks.basic_components import MarkdownTextObject, PlainTextObject
from slack_sdk.models.blocks.block_elements import ButtonElement

def build_error_home_view() -> View:
    return View(
        type="home",
        blocks=[
            SectionBlock(
                text=MarkdownTextObject(text="*:warning: Sorry, we couldn't load your information. Please try again later.*")
            )
        ]
    )

def build_home_view(
        student_info: dict,
        join_date: str,
        student_id: str
) -> View:
    display_middle = f" '{student_info['pname']}'" if student_info.get("pname") else ""
    student_name = f"{student_info['fname']}{display_middle} {student_info['lname']}"

    blocks: List[Block] = [
        # Student Information Section
        SectionBlock(
            text=MarkdownTextObject(text=f"*CTI Student:* {student_name}")
        ),
        SectionBlock(
            fields=[
                MarkdownTextObject(text=f"*Target Year:* {student_info['target_year']}"),
                MarkdownTextObject(text=f"*Join Date:* {join_date}"),
            ]
        ),
        ActionsBlock(
            elements=[
                ButtonElement(
                    text=PlainTextObject(text="View Student Information"),
                    action_id="view_student_info",
                    value=student_id,
                )
            ]
        ),
        DividerBlock(),

        # Emails Section
        SectionBlock(
            text=MarkdownTextObject(
                text=(
                    "*Registered Emails*\n\n"
                    "*Primary Email:* guerreronicolas1872@gmail.com\n"
                    "*Alternative Emails:* nicolas.guerrero@sjsu.edu, nicguerrero@csumb.edu"
                )
            )
        ),
        ActionsBlock(
            elements=[
                ButtonElement(
                    text=PlainTextObject(text="Update Emails"),
                    action_id="update_emails",
                    value=student_id,
                )
            ]
        ),
        DividerBlock(),

        # Attendance Section
        SectionBlock(
            text=MarkdownTextObject(
                text=(
                    "*Attendance*\n"
                    "Sessions attended this year: *20*\n"
                    "*Last Sessions Attended*\n"
                    "• October 31, 2025 (40% Interactions)\n"
                    "• November 6, 2025 (80% Interactions)\n"
                    "• November 14, 2025 (60% Interactions)"
                )
            )
        ),
        ActionsBlock(
            elements=[
                ButtonElement(
                    text=PlainTextObject(text="See Attendance History"),
                    action_id="see_attendance_history",
                    value=student_id,
                )
            ]
        ),
        DividerBlock(),

        # Badges Section
        SectionBlock(
            text=MarkdownTextObject(text="*Badge Progress* _(TODO: ignore for now)_")
        ),
        ImageBlock(
            image_url="https://picsum.photos/200",
            alt_text="Badge progress row",
        ),
        ActionsBlock(
            elements=[
                ButtonElement(
                    text=PlainTextObject(text="See Badges"),
                    action_id="see_badges",
                    value=student_id,
                )
            ]
        ),
    ]

    return View(type="home", blocks=blocks)
