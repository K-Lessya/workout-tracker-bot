from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import UpstreamMenuMoveTo
from ..callback_properties.movetos import TrainerMainMenuMoveTo
from app.callbacks.callbacks import MoveCallback
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from aiogram.types import WebAppInfo,WebAppData
from app.translations.base_translations import translations


def create_trainer_main_menu_keyboard(lang):
    builder = InlineKeyboardBuilder()
    builder_buttons = [
        {
            "text": translations[lang].trainer_main_menu_btn_add_client.value,
            "target": TrainerMainMenuMoveTo.add_client
        },
        {
            "text": translations[lang].trainer_main_menu_btn_my_clients.value,
            "target": TrainerMainMenuMoveTo.my_clients
        },
        {
            "text": translations[lang].trainer_main_menu_btn_exercise_db.value,
            "target": UpstreamMenuMoveTo.show_exercise_db
        },
        {
            "text": translations[lang].trainer_main_menu_btn_change_language.value,
            "target": TrainerMainMenuMoveTo.change_language
        }
    ]
    for button in builder_buttons:
            builder.button(
                text=button['text'], callback_data=MoveToCallback(move_to=button['target'])
            )
    webapp_info = WebAppInfo(url="https://aryzhykau.github.io/workout-tracker-bot/app/webapps/trainer-form/index.html")
    builder.row(InlineKeyboardButton(text=translations[lang].trainer_main_menu_btn_questionaire.value,
                                     callback_data=MoveCallback(target="to_no_content").pack()))
    builder.adjust(2, 1, 1)
    return builder.as_markup()
