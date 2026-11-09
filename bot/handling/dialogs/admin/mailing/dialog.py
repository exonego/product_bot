import logging

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Next, Back
from aiogram_dialog.widgets.input import TextInput, MessageInput

from bot.handling.states import MailingSG
from bot.handling.dialogs.admin.mailing.getters import (
    send_text_getter,
    send_media_getter,
    confirm_getter,
    started_getter,
)
from bot.handling.dialogs.admin.mailing.handlers import (
    back_to_start_handler,
    send_text_skip_handler,
    send_text_handler,
    back_to_send_text_handler,
    send_media_skip_handler,
    send_media_handler,
    confirm_mailing_handler,
)

logger = logging.getLogger(__name__)


mailing_dialog = Dialog(
    Window(
        Format("{admin_mailing_sendtext_text}"),
        Button(
            text=Format("{admin_button_back}"),
            id="back_to_start",
            on_click=back_to_start_handler,
        ),
        Next(
            text=Format("{admin_button_skip}"),
            id="send_text_skip",
            on_click=send_text_skip_handler,
        ),
        TextInput(id="send_text", on_success=send_text_handler),
        getter=send_text_getter,
        state=MailingSG.send_text,
    ),
    Window(
        Format("{admin_mailing_sendmedia_text}"),
        Back(
            text=Format("{admin_button_back}"),
            id="back_to_send_text",
            on_click=back_to_send_text_handler,
        ),
        Next(
            text=Format("{admin_button_skip}"),
            id="send_media_skip",
            on_click=send_media_skip_handler,
            when="text_not_skipped",
            show_mode=ShowMode.SEND,
        ),
        MessageInput(
            id="send_media",
            func=send_media_handler,
            content_types=[
                ContentType.PHOTO,
                ContentType.VIDEO,
                ContentType.VIDEO_NOTE,
            ],
        ),
        getter=send_media_getter,
        state=MailingSG.send_media,
    ),
    Window(
        Format("{admin_mailing_confirm_text}"),
        Back(text=Format("{admin_button_back}"), id="back_to_send_media"),
        Next(
            text=Format("{admin_button_confirm}"),
            id="confirm_mailing",
            on_click=confirm_mailing_handler,
        ),
        getter=confirm_getter,
        state=MailingSG.confirm,
    ),
    Window(
        Format("{admin_mailing_started_text}"),
        Button(
            text=Format("{admin_button_back}"),
            id="back_to_start_from_mailing_started",
            on_click=back_to_start_handler,
        ),
        getter=started_getter,
        state=MailingSG.started,
    ),
)
