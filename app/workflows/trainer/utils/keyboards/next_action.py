from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks.callbacks import MoveCallback
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.translations.base_translations import translations


class NextActionKeyboard(InlineKeyboardBuilder):
    def __init__(self, target, lang):
        super().__init__()
        self.row(InlineKeyboardButton(text=translations[lang].next_action_btn.value,
                                      callback_data=MoveCallback(target=target).pack()))