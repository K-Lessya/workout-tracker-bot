from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks.callbacks import MoveCallback
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.entities.training_plan.training_plan import DbTrainingDay
from app.entities.exercise.exercise import PlanTrainingExercise

class ClientPlanMenuKeyboard(InlineKeyboardBuilder):
    def __init__(self, client):
        super().__init__()
        self.row(
            InlineKeyboardButton(text="Просмотреть план",
                                 callback_data=MoveCallback(target=MyCLientsMoveTo.show_client_plan_days).pack()),
            InlineKeyboardButton(text="Создать новый план",
                                 callback_data=MoveToCallback(move_to=MyCLientsMoveTo.create_client_plan).pack())
        )
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client,
                                                                   option=str(client.id)).pack()))


class ClientPlanDaysKeyboard(InlineKeyboardBuilder):
    def __init__(self, plan_days: list[DbTrainingDay]):
        super().__init__()
        for idx, day in enumerate(plan_days):
            self.row(InlineKeyboardButton(text=f"День {idx+1}({day.name})",
                                          callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plan_day,
                                                                       option=str(idx)).pack()))
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=MyCLientsMoveTo.show_client_plan_menu).pack()))

class ClientPlanExercisesKeyboard(InlineKeyboardBuilder):
    def __init__(self, plan_day_exercises: list[PlanTrainingExercise]):
        super().__init__()
        for idx, exercise in enumerate(plan_day_exercises):
            self.row(InlineKeyboardButton(text=exercise.exercise.name,
                                          callback_data=ChooseCallback(
                                              target=TrainerMyClientsTargets.show_client_plan_exercise,
                                              option=str(idx)
                                          ).pack()))
        self.row(InlineKeyboardButton(text='Назад',
                                      callback_data=MoveCallback(target=MyCLientsMoveTo.show_client_plan_days).pack()))


class ClientPlanExerciseKeyboard(InlineKeyboardBuilder):
    def __init__(self, day: int):
        super().__init__()
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plan_day,
                                                                   option=str(day)).pack()))



