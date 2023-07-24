from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.choose_callback import ChooseCallback
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions, RegistrationCallbackTargets
from ..callback_properties import TrainerAddClientTargets, TrainerMainMenuTargets


def create_add_client_options_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="По ссылке или username", callback_data=ChooseCallback(target=TrainerAddClientTargets.by_username,
                                                                    option='')
    )
    builder.button(
        text="Поделившись контактом", callback_data=ChooseCallback(target=TrainerAddClientTargets.by_contact, option='')
    )
    builder.button(
        text="Выбрать из списка зарегистрированных", callback_data=ChooseCallback(
            target=TrainerAddClientTargets.by_existing,
            option='')
    )
    builder.button(text=f"Назад", callback_data=ChooseCallback(target=TrainerMainMenuTargets.go_to_main_menu,
                                                               option=''))
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()
