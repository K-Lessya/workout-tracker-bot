from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions, RegistrationCallbackTargets
from ..callback_properties.targets import TrainerAddClientTargets, TrainerMainMenuTargets
from app.entities.single_file.models import Client


def create_choose_existing_clients_keyboard(clients: list[Client]):
    builder = InlineKeyboardBuilder()
    for client in clients:
        builder.button(
            text=f"{client.name} {client.surname}", callback_data=ChooseCallback(
                target=TrainerAddClientTargets.show_clients,
                option=f'{client.tg_id}')
        )
    builder.button(text=f"Назад", callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu))
    return builder.as_markup()