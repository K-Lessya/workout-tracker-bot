from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..utils.callbacks.callbacks import CreateTrainingCallback, CreateTrainingCallbackActions


def create_add_exercise_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить упражнение", callback_data=CreateTrainingCallback(action=CreateTrainingCallbackActions.create_training)
    )
    builder.button(text='Сохранить', callback_data=CreateTrainingCallback(action=CreateTrainingCallbackActions.save))
    builder.button(text="Отмена", callback_data=CreateTrainingCallback(action=CreateTrainingCallbackActions.decline))
    return builder.as_markup()