from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utilities.default_callbacks.choose_callback import ChooseCallback
from app.workflows.client.utils.callback_properties import ClientMainMenuTargets, ClientMainMenuOptions


def create_client_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить тренировку", callback_data=ChooseCallback(target=ClientMainMenuTargets.create_training,
                                                                 option=ClientMainMenuOptions.new_training)
    )
    builder.button(
        text="Просмотреть тренировки", callback_data=ChooseCallback(target=ClientMainMenuTargets.show_training,
                                                                    option=ClientMainMenuOptions.show_training)
    )
    return builder.as_markup()