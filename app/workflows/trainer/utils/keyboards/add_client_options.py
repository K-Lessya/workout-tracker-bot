from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from app.callbacks.callbacks import MoveCallback
from app.workflows.common.utils.callback_properties.movetos import AddClientMoveTo, CommonGoBackMoveTo
from app.translations.base_translations import translations
from app.workflows.trainer.utils.callback_properties.movetos import TrainerMainMenuMoveTo


def create_add_client_options_keyboard(lang):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=translations[lang].trainer_add_client_btn_share_contact.value, callback_data=MoveToCallback(move_to=AddClientMoveTo.by_contact)
    )
    builder.button(
        text=translations[lang].trainer_add_client_btn_select_existed.value, callback_data=MoveToCallback(
            move_to=AddClientMoveTo.by_existing)
    )
    builder.button(text=translations[lang].go_back_btn.value, callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu))
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()



class AddClientByContactKeyboard(InlineKeyboardBuilder):
    def __init__(self, lang):
        super().__init__()
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=MoveToCallback(move_to=TrainerMainMenuMoveTo.add_client).pack()))

