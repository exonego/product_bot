import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Next, Back, Button
from aiogram_dialog.widgets.media import DynamicMedia

from bot_paid.handling.states import StepsSG
from bot_paid.handling.dialogs.user.steps.getters import (
    step1_getter,
    step2_getter,
    step3_getter,
    step4_getter,
    step5_getter,
    step6_getter,
    step7_getter,
)
from bot_paid.handling.dialogs.user.steps.handlers import (
    to_step6_handler,
    to_step7_handler,
)

logger = logging.getLogger(__name__)


steps_dialog = Dialog(
    Window(
        DynamicMedia(selector="step1_media"),
        Format("{paiduser_steps_step1_text_p1}"),
        Next(text=Format("{paiduser_steps_step1_button}")),
        getter=step1_getter,
        state=StepsSG.step1,
    ),
    Window(
        DynamicMedia(selector="step2_media"),
        Format("{paiduser_steps_step2_text_p1}"),
        Next(text=Format("{paiduser_steps_step2_button}")),
        Back(text=Format("{admin_button_back}")),
        getter=step2_getter,
        state=StepsSG.step2,
    ),
    Window(
        DynamicMedia(selector="step3_media"),
        Format("{paiduser_steps_step3_text_p1}"),
        Next(text=Format("{paiduser_steps_step3_button}")),
        Back(text=Format("{admin_button_back}")),
        getter=step3_getter,
        state=StepsSG.step3,
    ),
    Window(
        DynamicMedia(selector="step4_media"),
        Format("{paiduser_steps_step4_text_p1}"),
        Next(text=Format("{paiduser_steps_step4_button}")),
        Back(text=Format("{admin_button_back}")),
        getter=step4_getter,
        state=StepsSG.step4,
    ),
    Window(
        DynamicMedia(selector="step5_media"),
        Format("{paiduser_steps_step5_text_p1}"),
        Button(
            text=Format("{paiduser_steps_step5_button}"),
            id="next_step6",
            on_click=to_step6_handler,
        ),
        Back(text=Format("{admin_button_back}")),
        getter=step5_getter,
        state=StepsSG.step5,
    ),
    Window(
        Format("{paiduser_steps_step6_text_p4}"),
        Button(
            text=Format("{paiduser_steps_step6_button}"),
            id="next_step7",
            on_click=to_step7_handler,
        ),
        Back(text=Format("{admin_button_back}")),
        getter=step6_getter,
        state=StepsSG.step6,
    ),
    Window(
        Format("{paiduser_steps_step7_text_p2}"),
        Button(
            text=Format("{admin_button_back}"),
            id="back_step6",
            on_click=to_step6_handler,
        ),
        getter=step7_getter,
        state=StepsSG.step7,
    ),
)
