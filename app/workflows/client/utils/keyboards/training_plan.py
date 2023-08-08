from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientMyPlanTargets



class TrainingDaysKeyboard(InlineKeyboardBuilder):
    def __init__(self, days: list):
        super().__init__()
        for idx, day in enumerate(days):
            self.row(InlineKeyboardButton(text=f"День {idx+1} ({len(day.training_exercises)})",
                                          callback_data=ChooseCallback(
                                              target=ClientMyPlanTargets.show_day,
                                              option=str(idx)).pack()))
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_client_main_menu).pack()))


class TrainingDayExercises(InlineKeyboardBuilder):
    def __init__(self, exercises: list):
        super().__init__()
        for idx, exercise in enumerate(exercises):
            self.row(InlineKeyboardButton(text=f"{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}",
                                          callback_data=ChooseCallback(
                                              target=ClientMyPlanTargets.show_exercise,
                                              option=str(idx)).pack()))
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveToCallback(move_to=ClientMainMenuMoveTo.my_plan).pack()))

class PlanExerciseGoBackKeyboard(InlineKeyboardBuilder):
    def __init__(self, source_option):
        super().__init__()
        self.button(text='Назад',
                    callback_data=ChooseCallback(target=ClientMyPlanTargets.show_day, option=source_option).pack())

