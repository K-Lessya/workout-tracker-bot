from aiogram import Router
from .handler.add_client import add_client_router
from .handler.show_exercises import show_exercises_router
from .handler.add_exercise import add_exercise_router


trainer_router = Router()

trainer_router.include_routers(add_client_router, show_exercises_router, add_exercise_router)

