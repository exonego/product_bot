import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Next, Button
from aiogram_dialog.widgets.media import DynamicMedia

from bot.handling.states import UserMenuSG
from bot.handling.dialogs.user.menu.getters import (
    window1_getter,
    window2_getter,
    window3_getter,
    window4_getter,
)
from bot.handling.dialogs.user.menu.handlers import send_invoice_handler

logger = logging.getLogger(__name__)


menu_dialog = Dialog(
    Window(
        DynamicMedia(selector="window1_media"),
        Format("{user_menu_window1_text}"),
        Next(text=Format("{user_menu_window1_button}")),
        getter=window1_getter,
        state=UserMenuSG.window1,
    ),
    Window(
        DynamicMedia(selector="window2_media"),
        Format("{user_menu_window2_text}"),
        Next(text=Format("{user_menu_window2_button}")),
        getter=window2_getter,
        state=UserMenuSG.window2,
    ),
    Window(
        DynamicMedia(selector="window3_media"),
        Format("{user_menu_window3_text}"),
        Next(text=Format("{user_menu_window3_button}")),
        getter=window3_getter,
        state=UserMenuSG.window3,
    ),
    Window(
        DynamicMedia(selector="window4_media"),
        Format("{user_menu_window4_text}"),
        Button(
            text=Format("{user_menu_window4_button}"),
            id="window4_button",
            on_click=send_invoice_handler,
        ),
        getter=window4_getter,
        state=UserMenuSG.window4,
    ),
)
