from typing import Optional

from app.workflows.common.utils.keyboards.exercise_db_choose import ExerciseCommonListKeyboard
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from ..callback_properties.movetos import MyCLientsMoveTo
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.trainer.utils.callback_properties.movetos import ExerciseDbMoveTo
from ..callback_properties.targets import TrainerMyClientsTargets
from app.entities.exercise.exercise import *
from app.translations.base_translations import translations


class ExercisePlanListKeyboard(ExerciseCommonListKeyboard):
    def __init__(self, items: list[BodyPart | Exercise | MuscleGroup], exercises_length: int, tg_id: int, lang, day_id,
                 body_part_id=None):
        super().__init__(items=items, tg_id=tg_id)
        if items:
            if exercises_length >= 1 and isinstance(items[0], BodyPart):
                self.button(text=translations[lang].trainer_exercise_plan_list_keyboard_save_day.value,
                            callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plan_day, option=str(day_id)))


            # if isinstance(items[0], BodyPart):
            #     self.button(text=translations[lang].trainer_exercise_plan_list_keyboard_add_exercise.value,
            #             callback_data=MoveToCallback(move_to=ExerciseDbMoveTo.create_exercise))

            elif isinstance(items[0], MuscleGroup):
                self.button(text=translations[lang].go_back_btn.value,
                        callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_body_parts, option=""))

            elif isinstance(items[0], Exercise):
                self.button(text=translations[lang].go_back_btn.value,
                        callback_data=ChooseCallback(target=TrainerMyClientsTargets.choose_body_part, option=body_part_id).pack())
        else:
            self.button(text=translations[lang].trainer_exercise_plan_list_keyboard_save_day.value,
                        callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client_plan_day,
                                                     option=str(day_id)))
            # self.button(text=translations[lang].trainer_exercise_plan_list_keyboard_add_exercise.value,
            #             callback_data=MoveToCallback(move_to=ExerciseDbMoveTo.create_exercise))




        self.adjust(1, repeat=True)




