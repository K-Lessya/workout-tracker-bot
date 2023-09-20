from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from app.utilities.default_keyboards.choose import create_choose_keyboard
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.workflows.common.utils.callback_properties.movetos import ExerciseDbMoveTo
from app.workflows.trainer.utils.callback_properties.targets import CreateExerciseTargets
from typing import Optional
from app.entities.single_file.models import ClientRequests
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.translations.base_translations import translations


def create_go_back_button(move_to: ChooseCallback | MoveToCallback, lang):
    go_back_button = InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                          callback_data=move_to.pack())
    return go_back_button


def create_client_income_requests_keyboard(options: Optional[list[ClientRequests]], target: Optional[str],
                                           go_back_filter: ChooseCallback | MoveToCallback, lang):
    if options:
        return create_choose_keyboard(options=options,
                               additional_buttons=[create_go_back_button(go_back_filter, lang)],
                               option_attr='id', target=target)
    else:
        return create_choose_keyboard(options=None,
                                      target=None,
                                      option_attr=None,
                                      additional_buttons=[create_go_back_button(go_back_filter, lang)])
