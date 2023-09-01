from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from app.utilities.default_keyboards.choose import create_choose_keyboard
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.workflows.common.utils.callback_properties.movetos import ExerciseDbMoveTo
from app.workflows.trainer.utils.callback_properties.targets import CreateExerciseTargets
from app.workflows.common.utils.callback_properties.targets import ExerciseDbTargets
from typing import Optional
from app.entities.exercise.exercise import BodyPart, MuscleGroup, Exercise
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.entities.exercise.crud import *
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.workflows.client.utils.callback_properties.targets import ClientAddCustomTrainingTargets

add_exercise_button = InlineKeyboardButton(text=f'Добавить упражнение',
                                           callback_data=MoveToCallback(
                                             move_to=ExerciseDbMoveTo.create_exercise).pack())


def create_go_back_button(move_to: ChooseCallback | MoveToCallback):
    go_back_button = InlineKeyboardButton(text=f"Назад",
                                          callback_data=move_to.pack())
    print(move_to.pack())
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
        print("get_trainer")
        if options:
            if isinstance(options[0], BodyPart):
                if target == CreateExerciseTargets.process_body_part_name:
                    return create_choose_keyboard(options=options,
                                                  additional_buttons=[create_go_back_button(go_back_filter)],
                                                  option_attr='id', target=target)
                else:
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
            if target == ExerciseDbTargets.show_body_part:
                return create_choose_keyboard(options=None,
                                              target=None,
                                              option_attr=None,
                                              additional_buttons=[add_exercise_button,
                                                                  create_go_back_button(go_back_filter)])
            elif target == None:
                return create_choose_keyboard(options=None,
                                              target=None,
                                              option_attr=None,
                                              additional_buttons=[create_go_back_button(go_back_filter)]

                )




class ExerciseCommonListKeyboard(InlineKeyboardBuilder):
    def __init__(self, items: list[BodyPart | MuscleGroup | Exercise], tg_id: int):
        super().__init__()

        if isinstance(items[0], BodyPart):
            if get_trainer(tg_id=tg_id):
                target = TrainerMyClientsTargets.choose_body_part
            elif get_client_by_id(tg_id=tg_id):
                target = ClientAddCustomTrainingTargets.choose_body_parts

        elif isinstance(items[0], MuscleGroup):
            if get_trainer(tg_id=tg_id):
                target = TrainerMyClientsTargets.choose_muscle_group
            elif get_client_by_id(tg_id=tg_id):
                target = ClientAddCustomTrainingTargets.choose_muscle_group

        else:
            if get_trainer(tg_id=tg_id):
                target = TrainerMyClientsTargets.choose_exercise_for_plan
            elif get_client_by_id(tg_id=tg_id):
                target = ClientAddCustomTrainingTargets.choose_exercise

        for item in items:
            self.row(InlineKeyboardButton(text=f'{item.name}',
                        callback_data=ChooseCallback(
                            target=target,
                            option=str(item.id)).pack()))









