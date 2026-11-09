import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Row

from bot.handling.states import AdminMenuSG
from bot.handling.dialogs.admin.menu.getters import start_getter
from bot.handling.dialogs.admin.menu.handlers import (
    start_metrics_handler,
    start_price_handler,
    start_mailing_handler,
    leave_handler,
)

logger = logging.getLogger(__name__)


menu_dialog = Dialog(
    Window(
        Format("{admin_menu_text}"),
        Row(
            Button(
                text=Format("{admin_menu_button_metrics}"),
                id="start_metrics",
                on_click=start_metrics_handler,
            ),
            Button(
                text=Format("{admin_menu_button_mailing}"),
                id="start_mailing",
                on_click=start_mailing_handler,
            ),
        ),
        Row(
            Button(
                text=Format("{admin_menu_button_price}"),
                id="start_price",
                on_click=start_price_handler,
            ),
            Button(
                text=Format("{admin_menu_button_leave}"),
                id="leave",
                on_click=leave_handler,
            ),
        ),
        getter=start_getter,
        state=AdminMenuSG.menu,
    ),
)
