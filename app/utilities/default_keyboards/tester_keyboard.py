from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..default_callbacks.default_callbacks import TestCallback,TestTasks


def create_tester_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='Delete my user', callback_data=TestCallback(test_task=TestTasks.delete_me)),
    return builder.as_markup()
