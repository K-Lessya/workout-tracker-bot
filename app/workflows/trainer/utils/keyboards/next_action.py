from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks.callbacks import MoveCallback
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo


class NextActionKeyboard(InlineKeyboardBuilder):
    def __init__(self, target):
        super().__init__()
        self.row(InlineKeyboardButton(text="Далее",callback_data=MoveCallback(target=target).pack()))