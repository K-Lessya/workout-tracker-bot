from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from ..default_callbacks.choose_callback import ChooseCallback, YesNoOptions


def create_yes_no_keyboard(target):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да", callback_data=ChooseCallback(target=target, option=YesNoOptions.yes)
    )
    builder.button(
        text="Нет", callback_data=ChooseCallback(target=target, option=YesNoOptions.no)
    )
    return builder.as_markup()