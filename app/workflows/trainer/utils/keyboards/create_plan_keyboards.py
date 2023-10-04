from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.translations.base_translations import translations
from app.callbacks.callbacks import MoveCallback
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.utilities.default_callbacks.default_callbacks import ChooseCallback


class CreatePlanStartKeyboard(InlineKeyboardBuilder):
    def __init__(self, client_id, lang):
        super().__init__()
        self.row(InlineKeyboardButton(
            text=translations[lang].trainer_my_clients_single_client_create_plan_menu.value,
            callback_data=MoveCallback(target=MyCLientsMoveTo.add_day_to_plan).pack()
        ))
        self.row(InlineKeyboardButton(
            text=translations[lang].go_back_btn.value,
            callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client,
                                         option=str(client_id)).pack()
        ))
