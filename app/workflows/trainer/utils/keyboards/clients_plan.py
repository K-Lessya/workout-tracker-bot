from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks.callbacks import MoveCallback
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.entities.training_plan.training_plan import DbTrainingDay
from app.entities.exercise.exercise import PlanTrainingExercise
from app.translations.base_translations import translations


class ClientPlanMenuKeyboard(InlineKeyboardBuilder):
    def __init__(self, client, lang):
        formatted_date_string = '%d %m %Y'
        super().__init__()
        if client.training_plans:
            for idx, plan in enumerate(client.training_plans):
                self.row(InlineKeyboardButton(
                    text=plan.date.strftime(formatted_date_string),
                    callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plans, option=str(idx)).pack()
                ))
        self.row(
            InlineKeyboardButton(text=translations[lang].trainer_client_plan_menu_keyboard_create_new_plan.value,
                                 callback_data=MoveToCallback(move_to=MyCLientsMoveTo.create_client_plan).pack())
        )
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client,
                                                                   option=str(client.id)).pack()))


class ClientPlanDaysKeyboard(InlineKeyboardBuilder):
    def __init__(self, plan_days: list[DbTrainingDay], lang):
        super().__init__()
        for idx, day in enumerate(plan_days):
            self.row(InlineKeyboardButton(text=translations[lang].trainer_client_plan_days_keyboard_day_btn
                                          .value.format(idx+1, day.name),
                                          callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plan_day,
                                                                       option=str(idx)).pack()))
        self.row(InlineKeyboardButton(text=translations[lang].trainer_my_clients_single_client_create_plan_menu.value,
                                      callback_data=MoveCallback(target=MyCLientsMoveTo.add_day_to_plan).pack()))
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=MoveCallback(target=MyCLientsMoveTo.show_client_plan_menu).pack()))


class ClientPlanExercisesKeyboard(InlineKeyboardBuilder):
    def __init__(self, plan_day_exercises: list[PlanTrainingExercise], lang, plan_id):
        super().__init__()
        for idx, exercise in enumerate(plan_day_exercises):
            self.row(InlineKeyboardButton(text=exercise.exercise.name,
                                          callback_data=ChooseCallback(
                                              target=TrainerMyClientsTargets.show_client_plan_exercise,
                                              option=str(idx)
                                          ).pack()))
        self.row(InlineKeyboardButton(
            text=translations[lang].trainer_exercise_plan_list_keyboard_add_exercise.value,
            callback_data=MoveCallback(target=MyCLientsMoveTo.add_exercise_to_day).pack()
        ))
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plans, option=str(plan_id)).pack()))


class ClientPlanExerciseKeyboard(InlineKeyboardBuilder):
    def __init__(self, day: int, lang):
        super().__init__()
        #TODO
        # self.row(InlineKeyboardButton(
        #     text=translations[lang].trainer_my_clients_edit_plan_exercise_change_exercise.value,
        #     callback_data=MoveCallback(target=MyCLientsMoveTo.change_exercise).pack()
        # ))
        self.row(InlineKeyboardButton(
            text=translations[lang].trainer_my_clients_edit_plan_exercise_cange_runs.value,
            callback_data=MoveCallback(target=MyCLientsMoveTo.change_num_runs).pack()
        ))
        self.row(InlineKeyboardButton(
            text=translations[lang].trainer_my_clients_edit_plan_exercise_change_repeats.value,
            callback_data=MoveCallback(target=MyCLientsMoveTo.change_num_repeats).pack()
        ))
        self.row(InlineKeyboardButton(
            text=translations[lang].trainer_my_clients_edit_plan_exercise_change_trainer_note.value,
            callback_data=MoveCallback(target=MyCLientsMoveTo.change_trainer_note).pack()
        ))
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plan_day,
                                                                   option=str(day)).pack()))



