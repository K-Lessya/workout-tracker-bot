from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.callbacks.callbacks import ChooseCallback
from app.callbacks.options.default import YesNoOptions
from app.callbacks.targets.registration import RegistrationTargets
from app.callbacks.options.registration import RegistrationOptions
from app.translations.base_translations import translations


class YesNoKeyboard(InlineKeyboardBuilder):
    def __init__(self, target, lang):
        super().__init__()
        self.button(text=translations[lang].yes_no_btn_yes.value, callback_data=ChooseCallback(target=target, option=YesNoOptions.yes))
        self.button(text=translations[lang].yes_no_btn_no.value, callback_data=ChooseCallback(target=target, option=YesNoOptions.no))
        self.adjust(2)
