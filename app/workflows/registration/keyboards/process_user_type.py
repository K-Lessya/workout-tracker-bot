from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.choose_callback import ChooseCallback
from ..utils.callback_properties import ChooseUsrTypeOptions, RegistrationCallbackTargets


def create_choose_user_type_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Я Клиент", callback_data=ChooseCallback(target=RegistrationCallbackTargets.usr_type,
                                                      option=ChooseUsrTypeOptions.client)
    )
    builder.button(
        text="Я Тренер", callback_data=ChooseCallback(target=RegistrationCallbackTargets.usr_type,
                                                      option=ChooseUsrTypeOptions.trainer)
    )
    return builder.as_markup()
