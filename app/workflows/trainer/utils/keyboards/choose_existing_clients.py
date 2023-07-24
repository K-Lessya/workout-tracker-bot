from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.choose_callback import ChooseCallback
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions, RegistrationCallbackTargets
from ..callback_properties import TrainerAddClientTargets, TrainerMainMenuTargets
from app.entities.single_file.models import Client


def create_choose_existing_clients_keyboard(clients: list[Client]):
    builder = InlineKeyboardBuilder()
    for client in clients:
        builder.button(
            text=f"{client.name} {client.surname}", callback_data=ChooseCallback(
                target=TrainerMainMenuTargets.choose_existing_client,
                option=f'{client.tg_id}')
        )
    builder.button(text=f"Назад", callback_data=ChooseCallback(target=TrainerMainMenuTargets.go_to_main_menu,
                                                               option=''))
    return builder.as_markup()