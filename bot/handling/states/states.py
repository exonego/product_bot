from aiogram.fsm.state import State, StatesGroup


class UserMenuSG(StatesGroup):
    window1 = State()
    window2 = State()
    window3 = State()
    window4 = State()


class AdminMenuSG(StatesGroup):
    menu = State()
