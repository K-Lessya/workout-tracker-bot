from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import AddClientMoveTo, CommonGoBackMoveTo
from app.translations.base_translations import translations


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
