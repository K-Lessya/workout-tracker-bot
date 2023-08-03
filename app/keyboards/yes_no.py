from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.callbacks.callbacks import ChooseCallback
from app.callbacks.options.default import YesNoOptions
from app.callbacks.targets.registration import RegistrationTargets
from app.callbacks.options.registration import RegistrationOptions


class YesNoKeyboard(InlineKeyboardBuilder):
    def __init__(self, target):
        super().__init__()
        self.button(text="Да", callback_data=ChooseCallback(target=target, option=YesNoOptions.yes))
        self.button(text="Нет", callback_data=ChooseCallback(target=target, option=YesNoOptions.no))
        self.adjust(2)
