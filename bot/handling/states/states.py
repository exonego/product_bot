from aiogram.fsm.state import State, StatesGroup


class UserMenuSG(StatesGroup):
    window1 = State()
    window2 = State()
    window3 = State()
    window4 = State()


class AdminMenuSG(StatesGroup):
    menu = State()


class MetricsSG(StatesGroup):
    general = State()
    send_left = State()
    send_right = State()
    period = State()


class MailingSG(StatesGroup):
    send_media = State()
    send_text = State()
    confirm = State()
    started = State()


class PriceSG(StatesGroup):
    window = State()
