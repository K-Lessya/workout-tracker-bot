from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from aiogram.types import KeyboardButton
from aiogram.types import WebAppInfo
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.translations.base_translations import translations


class QuizKeyboard(InlineKeyboardBuilder):
    def __init__(self, lang):
        super().__init__()
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value, callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu).pack()))




