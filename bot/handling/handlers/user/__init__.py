from aiogram import Router

from .payment import payment_router

user_router = Router()
user_router.include_routers(payment_router)

__all__ = ["user_router"]
