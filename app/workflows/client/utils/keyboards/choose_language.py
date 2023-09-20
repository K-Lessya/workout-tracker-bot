from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.translations.base_translations import Languages, translations
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientChangeLanguageTarget
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback



class ChooseLanguageKeyboard(InlineKeyboardBuilder):
    def __init__(self, lang):
        super().__init__()
        for language in Languages:
            self.row(InlineKeyboardButton(text=language.value,
                                          callback_data=ChooseCallback(target=ClientChangeLanguageTarget.choose_language,
                                                                       option=language.name).pack()))
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_client_main_menu).pack()))
