from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.callbacks.callbacks import MoveCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientMyPlanTargets


class TrainingDaysKeyboard(InlineKeyboardBuilder):
    def __init__(self, days: list, target: str, go_back_target: str):
        super().__init__()
        for idx, day in enumerate(days):
            self.row(InlineKeyboardButton(text=f"День {idx+1} ({day.name})",
                                          callback_data=ChooseCallback(
                                              target=target,
                                              option=str(idx)).pack()))
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=go_back_target).pack()))


class TrainingDayExercises(InlineKeyboardBuilder):
    def __init__(self, exercises: list, target: str, go_back_target: str):
        super().__init__()
        for idx, exercise in enumerate(exercises):
            self.row(InlineKeyboardButton(text=f"{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}",
                                          callback_data=ChooseCallback(
                                              target=target,
                                              option=str(idx)).pack()))
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=go_back_target).pack()))


class PlanExerciseGoBackKeyboard(InlineKeyboardBuilder):
    def __init__(self, source_option, go_back_target: str):
        super().__init__()
        self.button(text='Назад',
                    callback_data=ChooseCallback(target=go_back_target, option=source_option).pack())

