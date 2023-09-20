from aiogram import Router
from .handlers.add_training.add_training import add_training_router
from .handlers.requests import client_request_router
from .handlers.client_main_menu import client_main_menu_router
from .handlers.my_plan import my_plan_router
from .handlers.my_trainings.my_trainings import my_trainings_router
from .handlers.my_trainer.handlers import client_my_trainer_router
from .handlers.add_training.custom import custom_training_router
from .handlers.change_language import client_change_language_router


client_router = Router()


client_router.include_routers(client_main_menu_router,
                              add_training_router,
                              client_request_router,
                              my_plan_router,
                              my_trainings_router,
                              client_my_trainer_router,
                              custom_training_router,
                              client_change_language_router)