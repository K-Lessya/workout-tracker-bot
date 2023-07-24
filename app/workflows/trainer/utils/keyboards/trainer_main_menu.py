from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utilities.default_callbacks.choose_callback import ChooseCallback
from app.workflows.trainer.utils.callback_properties import TrainerMainMenuTargets


def create_trainer_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder_buttons = [
        {
            "text": "Добавить клиента",
            "target": TrainerMainMenuTargets.add_client
        },
        {
            "text": "Мои клиенты",
            "target": TrainerMainMenuTargets.show_clients
        },
        {
            "text": "База упражнений",
            "target": TrainerMainMenuTargets.list_exercises
        }
    ]
    for button in builder_buttons:
            builder.button(
                text=button['text'], callback_data=ChooseCallback(target=button['target'], option='')
            )
    builder.adjust(2,1)
    return builder.as_markup()