import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Next, Back, SwitchTo
from aiogram_dialog.widgets.input import TextInput

from bot.handling.states import MetricsSG
from bot.handling.dialogs.admin.metrics.getters import (
    general_getter,
    sendleft_getter,
    sendright_getter,
    period_getter,
)
from bot.handling.dialogs.admin.metrics.handlers import (
    back_to_start_handler,
    sendleft_handler,
    sendright_handler,
)
from utils.checks import date_check

logger = logging.getLogger(__name__)


metrics_dialog = Dialog(
    Window(
        Format("{admin_metrics_general_text}"),
        Next(text=Format("{admin_metrics_general_button}")),
        Button(
            text=Format("{admin_button_back}"),
            id="back_to_start",
            on_click=back_to_start_handler,
        ),
        getter=general_getter,
        state=MetricsSG.general,
    ),
    Window(
        Format("{admin_metrics_sendleft_text}"),
        Back(text=Format("{admin_button_back}"), id="back_to_general"),
        TextInput(id="send_left", type_factory=date_check, on_success=sendleft_handler),
        getter=sendleft_getter,
        state=MetricsSG.send_left,
    ),
    Window(
        Format("{admin_metrics_sendright_text}"),
        Back(text=Format("{admin_button_back}"), id="back_to_send_left"),
        TextInput(
            id="send_right", type_factory=date_check, on_success=sendright_handler
        ),
        getter=sendright_getter,
        state=MetricsSG.send_right,
    ),
    Window(
        Format("{admin_metrics_period_text}"),
        SwitchTo(
            text=Format("{admin_button_back}"),
            id="switch_to_general",
            state=MetricsSG.general,
        ),
        getter=period_getter,
        state=MetricsSG.period,
    ),
)
