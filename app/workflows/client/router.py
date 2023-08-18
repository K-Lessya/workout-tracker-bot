from aiogram import Router
from .handlers.add_training.add_training import add_training_router
from .handlers.requests import client_request_router
from .handlers.client_main_menu import client_main_menu_router
from .handlers.my_plan import my_plan_router

client_router = Router()


client_router.include_routers(client_main_menu_router, add_training_router, client_request_router, my_plan_router)