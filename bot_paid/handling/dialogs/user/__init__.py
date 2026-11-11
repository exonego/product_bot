from aiogram import Router

from .steps import steps_dialog

dialog_user_router = Router()
dialog_user_router.include_routers(steps_dialog)

__all__ = ["dialog_user_router"]
