from aiogram import Router
from .handlers.add_client import add_client_router
from .handlers.add_exercise import add_exercise_router



trainer_router = Router()

trainer_router.include_routers(add_client_router, add_exercise_router)
