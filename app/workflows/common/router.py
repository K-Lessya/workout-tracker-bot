from aiogram import Router
from .handlers.show_exercises_db import show_exercises_db_router

common_router = Router()

common_router.include_routers(show_exercises_db_router)