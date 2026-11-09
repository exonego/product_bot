import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput

from bot.handling.states import PriceSG
from bot.handling.dialogs.admin.price.getters import window_getter
from bot.handling.dialogs.admin.price.handlers import (
    back_to_start_handler,
    correct_price_handler,
)
from utils.checks import price_check

logger = logging.getLogger(__name__)


price_dialog = Dialog(
    Window(
        Format("{admin_price_window_text}"),
        Button(
            text=Format("{admin_button_back}"),
            id="back_to_start",
            on_click=back_to_start_handler,
        ),
        TextInput(
            id="price_input", type_factory=price_check, on_success=correct_price_handler
        ),
        getter=window_getter,
        state=PriceSG.window,
    ),
)
