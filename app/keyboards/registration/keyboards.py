from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.callbacks.callbacks import ChooseCallback
from app.callbacks.targets.registration import RegistrationTargets
from app.callbacks.options.registration import RegistrationOptions


class ChooseUsrTypeKeyboard(InlineKeyboardBuilder):
    def __init__(self):
        super().__init__()
        self.row(
            InlineKeyboardButton(text="Я клиент",
                                 callback_data=ChooseCallback(target=RegistrationTargets.choose_user_type,
                                                              option=RegistrationOptions.client).pack()),
            InlineKeyboardButton(text="Я тренер",
                                 callback_data=ChooseCallback(target=RegistrationTargets.choose_user_type,
                                                              option=RegistrationOptions.trainer).pack())
        )
