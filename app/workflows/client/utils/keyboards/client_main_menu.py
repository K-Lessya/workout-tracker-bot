from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from ..callback_properties.movetos import ClientMainMenuMoveTo
from app.entities.single_file.crud import client_get_num_trainier_requests
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.entities.single_file.models import Client
from app.callbacks.callbacks import MoveCallback


def create_client_main_menu_keyboard(client: Client):
    builder = InlineKeyboardBuilder()
    builder_buttons = [
        {
            "text": f"Мои заявки({client_get_num_trainier_requests(client=client)})",
            "target": ClientMainMenuMoveTo.my_recieved_requests
        },
        {
            "text": "Мои тренировки",
            "target": ClientMainMenuMoveTo.my_trainings
        },
        {
            "text": "Добавить тренировку",
            "target": ClientMainMenuMoveTo.add_training
        },
        {
            "text": "Мой тренер",
            "target": "to_no_content"
        },
        {
            "text": "Мой план",
            "target": ClientMainMenuMoveTo.my_plan
        }

    ]

    for button in builder_buttons:
        if not client.trainings and button['text'] == "Мои тренировки":
            pass
        elif not client.training_plan and button['text'] == "Мой план":
            pass
        else:
            builder.button(
                text=button['text'], callback_data=MoveCallback(target=button['target'])
            )
    if len(builder_buttons) == 5:
        builder.adjust(2, 2, 1)
    elif len(builder_buttons) == 4:
        builder.adjust(2, 2)
    elif len(builder_buttons) == 3:
        builder.adjust(2, 1)
    return builder.as_markup()
