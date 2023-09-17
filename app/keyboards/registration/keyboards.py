from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.callbacks.callbacks import ChooseCallback
from app.callbacks.targets.registration import RegistrationTargets
from app.callbacks.options.registration import RegistrationOptions
from app.translations.base_translations import Languages
from app.translations.base_translations import translations


class ChooseUsrTypeKeyboard(InlineKeyboardBuilder):
    def __init__(self, lang):
        super().__init__()
        self.row(
            InlineKeyboardButton(text=translations[lang].usr_type_btn_client.value,
                                 callback_data=ChooseCallback(target=RegistrationTargets.choose_user_type,
                                                              option=RegistrationOptions.client).pack()),
            InlineKeyboardButton(text=translations[lang].usr_type_btn_trainer.value,
                                 callback_data=ChooseCallback(target=RegistrationTargets.choose_user_type,
                                                              option=RegistrationOptions.trainer).pack())
        )


class ChooseLanguageKeyboard(InlineKeyboardBuilder):
    def __init__(self):
        super().__init__()
        for lang in Languages:
            self.row(InlineKeyboardButton(text=lang.value, callback_data=ChooseCallback(target=RegistrationTargets.choose_user_language,
                                                                                        option=lang.name).pack()))

