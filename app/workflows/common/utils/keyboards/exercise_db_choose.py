from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from app.utilities.default_keyboards.choose import create_choose_keyboard
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.workflows.common.utils.callback_properties.movetos import ExerciseDbMoveTo, UpstreamMenuMoveTo
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
from app.translations.base_translations import translations
from app.config import CHOOSE_BUTTON_MAX_COUNT_PER_PAGE


def create_add_exercise_button(lang):

    add_exercise_button = InlineKeyboardButton(text=translations[lang].trainer_add_exercise_btn_add_exercise.value,
                                               callback_data=MoveToCallback(
                                                 move_to=ExerciseDbMoveTo.create_exercise).pack())
    return add_exercise_button


def create_go_back_button(move_to: ChooseCallback | MoveToCallback, lang):
    go_back_button = InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                          callback_data=move_to.pack())
    print(move_to.pack())
    return go_back_button


def create_exercise_db_choose_keyboard(options: Optional[list[BodyPart | MuscleGroup | Exercise]],
                                       source: Message | CallbackQuery, target: Optional[str],
                                       go_back_filter: ChooseCallback | MoveToCallback, lang):
    user = source.from_user.id

    if get_client_by_id(user):
        if options:
            return create_choose_keyboard(options=options,
                                   additional_buttons=[create_go_back_button(go_back_filter, lang=lang)],
                                   option_attr='id', target=target)
        else:
            return create_choose_keyboard(options=None,
                                          target=None,
                                          option_attr=None,
                                          additional_buttons=[create_go_back_button(go_back_filter, lang=lang)])
    elif get_trainer(user):
        print("get_trainer")
        if options:
            if isinstance(options[0], BodyPart):
                if target == CreateExerciseTargets.process_body_part_name:
                    return create_choose_keyboard(options=options,
                                                  additional_buttons=[create_go_back_button(go_back_filter, lang=lang)],
                                                  option_attr='id', target=target)
                else:
                    return create_choose_keyboard(options=options,
                                       additional_buttons=[create_add_exercise_button(lang),
                                                           create_go_back_button(go_back_filter, lang=lang)],
                                       option_attr='id', target=target)
            else:
                return create_choose_keyboard(options=options,
                                              additional_buttons=[create_go_back_button(
                                                                      go_back_filter, lang=lang)],
                                              option_attr='id', target=target)
        else:
            if target == ExerciseDbTargets.show_body_part:
                return create_choose_keyboard(options=None,
                                              target=None,
                                              option_attr=None,
                                              additional_buttons=[create_add_exercise_button(lang),
                                                                  create_go_back_button(go_back_filter, lang=lang)])
            elif target == "Exercise":
                return create_choose_keyboard(options=None,
                                              target=None,
                                              option_attr=None,
                                              additional_buttons=[create_go_back_button(go_back_filter, lang=lang)]

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





class CategoryPaginationKeyboard:

    start_index: int
    count: int
    options: list
    target: str
    lang: str
    option_attr: any
    ui: InlineKeyboardBuilder

    def __init__(self, options, target, option_attr, count, start_index, lang, go_back_callback_data,
                 additional_btns=list):
        super().__init__()
        self.start_index = start_index
        self.count = count
        self.options = options
        self.target = target
        self.option_attr = option_attr
        self.lang = lang
        self.go_back_callback_data = go_back_callback_data
        self.draw_keyboard(additional_btns=additional_btns)

    def draw_keyboard(self, additional_btns):
        self.ui = InlineKeyboardBuilder()
        options_list = []
        for option in self.options:
            options_list.append(option)
        if len(options_list) < self.count:
            for option in options_list:
                self.ui.row(InlineKeyboardButton(
                    text=option.name,
                    callback_data=ChooseCallback(target=self.target, option=str(getattr(option, self.option_attr))).pack()
                ))
        else:
            for option in options_list[self.start_index:self.start_index+self.count:1]:
                self.ui.row(InlineKeyboardButton(
                    text=option.name,
                    callback_data=ChooseCallback(target=self.target, option=str(getattr(option, self.option_attr))).pack()
                ))
            move_buttons = []
            if self.start_index > 0:
                move_buttons.append(
                    InlineKeyboardButton(
                        text="<<",
                        callback_data=MoveToCallback(move_to="prev").pack()
                    )
                )
            if self.start_index+self.count-1 < len(self.options)-1:
                move_buttons.append(
                    InlineKeyboardButton(
                        text=">>",
                        callback_data=MoveToCallback(move_to="next").pack()
                    )
                )
            self.ui.row(*move_buttons)
            if additional_btns:
                self.ui.row(*additional_btns)
            self.ui.row(InlineKeyboardButton(
                text=translations[self.lang].go_back_btn.value,
                callback_data=self.go_back_callback_data.pack()
            ))

    def list_forward(self):
        self.start_index += self.count
        self.draw_keyboard()

    def list_backward(self):
        self.start_index -= self.count
        self.draw_keyboard()


class BodyPartsKeyboard(CategoryPaginationKeyboard):

    def __init__(self, body_parts, start_index, lang, create_exercise_btn: bool):
        go_back_callback = MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu)
        if create_exercise_btn:
            additional_btns = [
                InlineKeyboardButton(
                    text=translations[lang].trainer_add_exercise_btn_add_exercise.value,
                    callback_data=
                )
            ]
        super().__init__(body_parts, ExerciseDbTargets.show_body_part, 'id', 1, start_index, lang, go_back_callback)


class MuscleGroupsKeyboard(CategoryPaginationKeyboard):

    def __init__(self, muscle_groups, start_index, lang):
        go_back_callback = MoveToCallback(move_to=UpstreamMenuMoveTo.show_exercise_db)
        super().__init__(muscle_groups, ExerciseDbTargets.show_muscle_group, 'id', 1, start_index, lang, go_back_callback)

class ExercisesListKeyboard(CategoryPaginationKeyboard):

    def __init__(self, exercises, start_index, source_option, lang):
        go_back_callback = ChooseCallback(target=ExerciseDbTargets.show_body_part, option=source_option)
        super().__init__(exercises, ExerciseDbTargets.show_exercise, 'id', 1, start_index, lang,
                         go_back_callback)

class ExerciseKeyboard(InlineKeyboardBuilder):
    def __init__(self, exercise, source_option, lang):
        super().__init__()
        self.row(
            InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                 callback_data=ChooseCallback(target=ExerciseDbTargets.show_muscle_group,
                                                              option=source_option).pack())
        )
















