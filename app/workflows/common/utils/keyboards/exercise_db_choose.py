from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from app.utilities.default_keyboards.choose import create_choose_keyboard
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.workflows.common.utils.callback_properties.movetos import ExerciseDbMoveTo
from typing import Optional
from app.entities.exercise.exercise import BodyPart, MuscleGroup, Exercise
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo


add_exercise_button = InlineKeyboardButton(text=f'Добавить упражнение',
                                           callback_data=MoveToCallback(
                                             move_to=ExerciseDbMoveTo.create_exercise).pack())


def create_go_back_button(move_to: ChooseCallback | MoveToCallback):
    go_back_button = InlineKeyboardButton(text=f"Назад",
                                          callback_data=move_to.pack())
    return go_back_button


def create_exercise_db_choose_keyboard(options: Optional[list[BodyPart | MuscleGroup | Exercise]],
                                       source: Message | CallbackQuery, target: Optional[str],
                                       go_back_filter: ChooseCallback | MoveToCallback):
    user = source.from_user.id

    if get_client_by_id(user):
        if options:
            return create_choose_keyboard(options=options,
                                   additional_buttons=[create_go_back_button(go_back_filter)],
                                   option_attr='id', target=target)
        else:
            return create_choose_keyboard(options=None,
                                          target=None,
                                          option_attr=None,
                                          additional_buttons=[create_go_back_button(go_back_filter)])
    elif get_trainer(user):
        if options:
            if isinstance(options[0], BodyPart):
                return create_choose_keyboard(options=options,
                                   additional_buttons=[add_exercise_button,
                                                       create_go_back_button(go_back_filter)],
                                   option_attr='id', target=target)
            else:
                return create_choose_keyboard(options=options,
                                              additional_buttons=[create_go_back_button(
                                                                      go_back_filter)],
                                              option_attr='id', target=target)
        else:
            return create_choose_keyboard(options=None,
                                          target=None,
                                          option_attr=None,
                                          additional_buttons=[create_go_back_button(go_back_filter)])
