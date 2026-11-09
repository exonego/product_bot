from aiogram import Router

from bot.handling.filters import RoleFilter
from bot.enums import Role

from .menu import menu_dialog
from .metrics import metrics_dialog
from .price import price_dialog
from .mailing import mailing_dialog

dialog_admin_router = Router()
dialog_admin_router.message.filter(RoleFilter(Role.ADMIN))
dialog_admin_router.callback_query.filter(RoleFilter(Role.ADMIN))
dialog_admin_router.include_routers(
    menu_dialog, metrics_dialog, price_dialog, mailing_dialog
)

__all__ = ["dialog_admin_router"]
