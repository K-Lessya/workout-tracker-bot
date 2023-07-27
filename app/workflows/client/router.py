from aiogram import Router
from .handlers.add_training import add_training_router
from .handlers.requests import client_request_router

client_router = Router()


client_router.include_routers(add_training_router, client_request_router)