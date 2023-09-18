from app.workflows.common.utils.keyboards.exercise_db_choose import ExerciseCommonListKeyboard
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from ..callback_properties.movetos import MyCLientsMoveTo
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.trainer.utils.callback_properties.movetos import ExerciseDbMoveTo
from ..callback_properties.targets import TrainerMyClientsTargets
from app.entities.exercise.exercise import *
from app.translations.base_translations import translations


class ExercisePlanListKeyboard(ExerciseCommonListKeyboard):
    def __init__(self, items: list[BodyPart | Exercise | MuscleGroup], day_num: int, exercises_length: int, tg_id: int, lang):
        super().__init__(items=items, tg_id=tg_id)
        if exercises_length >= 1 and isinstance(items[0], BodyPart):
            self.button(text=translations[lang].trainer_exercise_plan_list_keyboard_save_day.value.format(day_num),
                        callback_data=MoveToCallback(move_to=MyCLientsMoveTo.save_client_day))

        if isinstance(items[0], BodyPart):
            self.button(text=translations[lang].trainer_exercise_plan_list_keyboard_add_exercise.value,
                        callback_data=MoveToCallback(move_to=ExerciseDbMoveTo.create_exercise))
        elif isinstance(items[0], MuscleGroup):
            self.button(text=translations[lang].go_back_btn.value,
                        callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_body_parts, option=""))

        else:
            self.button(text=translations[lang].go_back_btn.value,
                        callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu))

        self.adjust(1, repeat=True)




