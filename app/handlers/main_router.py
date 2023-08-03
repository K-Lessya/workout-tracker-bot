from aiogram import Router
from app.handlers.registration.handlers import registration_router


main_router = Router()

main_router.include_routers(registration_router)