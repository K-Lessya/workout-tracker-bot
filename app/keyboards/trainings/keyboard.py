from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.callbacks.callbacks import MoveCallback
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from typing import Optional
from app.keyboards.menus.classes import MenuOption
from app.buttons.go_back import GoBackButton
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo, MyTrainingsMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientMyTrainingsTarget
from app.translations.base_translations import translations


class PaginationKeyboard(InlineKeyboardBuilder):
    def __init__(self, options: list, list_length: int, first_index: int, last_index: int, lang, prev_target: str,
                 next_target: str, go_back_target: str, go_back_to_choose=False, choose_option=''):
        super().__init__()
        for option in options:
            self.row(InlineKeyboardButton(text=option.text, callback_data=ChooseCallback(target=option.target,
                                                                                         option=option.option).pack()))
        buttons = []
        if first_index > 0 and list_length > 4:
            buttons.append(InlineKeyboardButton(text='<<', callback_data=MoveCallback(target=prev_target).pack()))
        if go_back_to_choose:
            buttons.append(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                                callback_data=ChooseCallback(target=go_back_target,
                                                                             option=choose_option).pack()))
        else:
            buttons.append(InlineKeyboardButton(text=translations[lang].go_back_btn.value, callback_data=MoveCallback(target=go_back_target).pack()))
        if last_index < list_length-1 and list_length > 4:
            buttons.append(InlineKeyboardButton(text='>>', callback_data=MoveCallback(target=next_target).pack()))
        self.row(*buttons)


class TrainingExercisesKeyboard(InlineKeyboardBuilder):
    def __init__(self, target, go_back_target, exercises, lang):
        super().__init__()
        for idx, exercise in enumerate(exercises):
            self.row(InlineKeyboardButton(text=exercise.exercise.name,
                                          callback_data=ChooseCallback(target=target,
                                                                       option=str(idx)).pack()))
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=MoveCallback(target=go_back_target).pack()))


class TrainingSingleExerciseKeyboard(InlineKeyboardBuilder):
    def __init__(self, has_video: bool, target, go_back_target, source_option, lang):
        super().__init__()
        if has_video:
            self.row(InlineKeyboardButton(text=translations[lang]
                                          .trainer_client_training_exercise_show_video_with_comments.value,
                                          callback_data=MoveCallback(target=target).pack()))
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=ChooseCallback(target=go_back_target,
                                                                   option=source_option).pack()))


class TrainingVideoKeyboard(InlineKeyboardBuilder):
    def __init__(self, go_back_target, source_option, lang):
        super().__init__()
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=ChooseCallback(target=go_back_target,
                                                                   option=source_option).pack()))





