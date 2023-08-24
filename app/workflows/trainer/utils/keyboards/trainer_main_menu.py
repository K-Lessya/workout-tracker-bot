from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import UpstreamMenuMoveTo
from ..callback_properties.movetos import TrainerMainMenuMoveTo
from aiogram.types import WebAppInfo,WebAppData


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
    webapp_info = WebAppInfo(url="https://localhost:8086")
    builder.row(InlineKeyboardButton(text="Анкета для клиентов", web_app=webapp_info))
    builder.adjust(2, 1, 1)
    return builder.as_markup()
