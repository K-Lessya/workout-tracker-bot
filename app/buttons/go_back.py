from aiogram.types import InlineKeyboardButton
from app.callbacks.callbacks import MoveCallback


class GoBackButton(InlineKeyboardButton):
    def __init__(self, text, target):
        super().__init__()
        self.callback_data = MoveCallback(target=target).pack()
        self.text = text
