from aiogram import Router
from .handlers.add_client import add_client_router
from .handlers.add_exercise import add_exercise_router
from .handlers.my_clients import my_clients_router
from .handlers.quiz import quiz_router
from .handlers.client_plan.handlers import client_plan_router
from .handlers.change_language import trainer_change_language_router



trainer_router = Router()

trainer_router.include_routers(add_client_router, add_exercise_router, my_clients_router, quiz_router,
                               client_plan_router, trainer_change_language_router)
