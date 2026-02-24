import time

from typing import List

from slack_sdk.models.views import View
from slack_sdk.models.blocks import (
    Block,
    HeaderBlock,
    ImageElement,
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
        student_id: str,
) -> View:
    display_middle = f" '{student_info['pname']}'" if student_info.get("pname") else ""
    student_name = f"*{student_info['fname']}{display_middle} {student_info['lname']}*"
    last_updated = int(time.time())

    blocks: List[Block] = [
        HeaderBlock(text=PlainTextObject(text="CTI Student Dashboard")),

        # Student Information Section
        SectionBlock(
            text=MarkdownTextObject(text=f":bust_in_silhouette: {student_name}")
        ),
        SectionBlock(
            fields=[
                MarkdownTextObject(text=f":date: *Target Year:* {student_info['target_year']}"),
                MarkdownTextObject(text=f":spiral_calendar_pad: *Join Date:* {join_date}"),
            ],
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
                    ":email: *Registered Emails*\n\n"
                    "*Primary Email:* primary.email@gmail.com\n"
                    "*Alternative Emails:* temp@email.edu, temp.edu@email.edu"
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
                    ":chart_with_upwards_trend: *Attendance & Interactions*\n"
                    "Sessions Attended This Year: *20*\n\n"
                    "*Last Sessions Attended*\n"
                    "• October 31, 2025: :large_yellow_circle: 40%\n"
                    "• November 6, 2025: :large_green_circle: 80%\n"
                    "• November 14, 2025: :large_yellow_circle: 60%"
                ),
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
            text=MarkdownTextObject(text="*Badge Progress*")
        ),
        # NOTE -- leaving these out for now as we don't have badge data nor can they be formatted side-by-side without an external library
        # ImageBlock(
        #     image_url="https://picsum.photos/100",
        #     alt_text="Badge progress row",
        # ),
        # ImageBlock(
        #     image_url="https://picsum.photos/100",
        #     alt_text="Badge progress row",
        # ),
        # ImageBlock(
        #     image_url="https://picsum.photos/100",
        #     alt_text="Badge progress row",
        # ),
        ActionsBlock(
            elements=[
                ButtonElement(
                    text=PlainTextObject(text="See Badges"),
                    action_id="see_badges",
                    value=student_id,
                )
            ]
        ),

        DividerBlock(),

        # Footer with last updated timestamp
        SectionBlock(
            fields=[
                MarkdownTextObject(text=f"*Last Updated:* <!date^{last_updated}^{{date_pretty}} at {{time}}|{time.ctime(last_updated)} UTC>"),
            ]
        ),
        ActionsBlock(
            elements=[
                ButtonElement(
                    text=PlainTextObject(text=":arrows_counterclockwise: Refresh"),
                    action_id="handle_refresh",
                    value=student_id,
                )
            ]
        )
    ]

    return View(type="home", blocks=blocks)
