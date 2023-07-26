from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import AddClientMoveTo, CommonGoBackMoveTo



def create_add_client_options_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="По ссылке", callback_data=MoveToCallback(move_to=AddClientMoveTo.by_username)
    )
    builder.button(
        text="Поделившись контактом", callback_data=MoveToCallback(move_to=AddClientMoveTo.by_contact)
    )
    builder.button(
        text="Выбрать из списка зарегистрированных", callback_data=MoveToCallback(
            move_to=AddClientMoveTo.by_existing)
    )
    builder.button(text=f"Назад", callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu))
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()
