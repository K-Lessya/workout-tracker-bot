from app.entities.training_plan.crud import get_client_active_plans
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from ..callback_properties.movetos import ClientMainMenuMoveTo
from app.entities.single_file.crud import client_get_num_trainier_requests
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.entities.single_file.models import Client
from app.callbacks.callbacks import MoveCallback
from app.translations.base_translations import translations


def create_client_main_menu_keyboard(client: Client, lang):
    builder = InlineKeyboardBuilder()
    builder_buttons = [
        {
            "text": translations[lang].client_menu_btn_add_training.value,
            "target": ClientMainMenuMoveTo.add_training
        },
        {
            "text": translations[lang].client_main_menu_btn_my_requests.value.format(client_get_num_trainier_requests(client=client)),
            "target": ClientMainMenuMoveTo.my_recieved_requests
        },
        {
            "text": translations[lang].client_main_menu_btn_my_trainings.value,
            "target": ClientMainMenuMoveTo.my_trainings
        },

        {
            "text": translations[lang].client_main_menu_btn_my_trainer.value,
            "target": ClientMainMenuMoveTo.my_trainer
        },
        {
            "text": translations[lang].client_main_menu_btn_my_plan.value,
            "target": ClientMainMenuMoveTo.my_plan
        },
        {
            "text": translations[lang].trainer_main_menu_btn_change_language.value,
            "target": ClientMainMenuMoveTo.change_language
        }

    ]

    for button in builder_buttons:
        if not client.trainings and button['text'] == translations[lang].client_main_menu_btn_my_trainings.value:
            pass
        elif not get_client_active_plans(client.tg_id) and button['text'] == translations[lang].client_main_menu_btn_my_plan.value:
            pass
        else:
            builder.button(
                text=button['text'], callback_data=MoveCallback(target=button['target'])
            )
    if len(builder_buttons) == 6:
        builder.adjust(1, 2, 2, 1)
    elif len(builder_buttons) == 5:
        builder.adjust(1, 2, 1,1)
    elif len(builder_buttons) == 4:
        builder.adjust(1, 2,1)
    return builder.as_markup()
