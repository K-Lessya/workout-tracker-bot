from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.callback_types import ChooseCallback, ChooseCallbackOptions, ChooseCallbackTargets


def create_choose_user_type_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Я Клиент", callback_data=ChooseCallback(target=ChooseCallbackTargets.usr_type,
                                                      option=ChooseCallbackOptions.client)
    )
    builder.button(
        text="Я Тренер", callback_data=ChooseCallback(target=ChooseCallbackTargets.usr_type,
                                                      option=ChooseCallbackOptions.trainer)
    )
    return builder.as_markup()
