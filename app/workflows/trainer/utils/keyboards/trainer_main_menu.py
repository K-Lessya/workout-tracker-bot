from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import UpstreamMenuMoveTo
from ..callback_properties.movetos import TrainerMainMenuMoveTo


def create_trainer_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder_buttons = [
        {
            "text": "Добавить клиента",
            "target": TrainerMainMenuMoveTo.add_client
        },
        {
            "text": "Мои клиенты",
            "target": TrainerMainMenuMoveTo.my_clients
        },
        {
            "text": "База упражнений",
            "target": UpstreamMenuMoveTo.show_exercise_db
        }
    ]
    for button in builder_buttons:
            builder.button(
                text=button['text'], callback_data=MoveToCallback(move_to=button['target'])
            )
    builder.adjust(2, 1)
    return builder.as_markup()
