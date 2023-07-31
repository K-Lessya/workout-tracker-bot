from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from ..default_callbacks.default_callbacks import ChooseCallback, YesNoOptions


def create_yes_no_keyboard(target):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да", callback_data=ChooseCallback(target=target, option=YesNoOptions.yes)
    )
    builder.button(
        text="Нет", callback_data=ChooseCallback(target=target, option=YesNoOptions.no)
    )
    return builder.as_markup()


class YesNoKeyboard(InlineKeyboardBuilder):
    def __init__(self, target):
        super().__init__()
        self.button(
            text="Да", callback_data=ChooseCallback(target=target, option=YesNoOptions.yes)
        )
        self.button(
            text="Нет", callback_data=ChooseCallback(target=target, option=YesNoOptions.no)
        )