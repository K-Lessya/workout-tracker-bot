from app.workflows.common.utils.keyboards.exercise_db_choose import ExerciseCommonListKeyboard
from app.utilities.default_callbacks.default_callbacks import MoveToCallback
from ..callback_properties.movetos import MyCLientsMoveTo
from ..callback_properties.targets import TrainerMyClientsTargets
from app.entities.exercise.exercise import *


class ExercisePlanListKeyboard(ExerciseCommonListKeyboard):
    def __init__(self, items: list[BodyPart | Exercise | MuscleGroup], day_num: int, exercises_length: int):
        super().__init__(items=items)
        if exercises_length >= 1 and isinstance(items[0], BodyPart):
            self.button(text=f'Сохранить день {day_num}',
                        callback_data=MoveToCallback(move_to=MyCLientsMoveTo.save_client_day))

        self.button(text='Назад(Не работает)', callback_data='no')

        self.adjust(1, repeat=True)




