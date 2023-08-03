from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.callbacks.callbacks import MoveCallback
from app.keyboards.menus.classes import MenuOption


class MenuKeyboard(InlineKeyboardBuilder):
    def __init__(self, menu_options: MenuOption):
        super().__init__()
        for option in menu_options:
            self.row(InlineKeyboardButton(
                text=menu_options.text,
                target=MoveCallback(target=menu_options.target)
            ))