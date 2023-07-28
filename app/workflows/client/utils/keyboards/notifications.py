from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..callback_properties.targets import ClientIncomeRequestTargets
from app.utilities.default_callbacks.default_callbacks import ChooseCallback


def create_new_trainer_request_keyboard(trainer_id: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="Просмотреть заявку", callback_data=ChooseCallback(target=ClientIncomeRequestTargets.show_income_request,
                                                                           option=trainer_id))
    builder.adjust(1)
    return builder.as_markup()