from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.workflows.client.utils.callback_property import CreateTrainingCallback, CreateTrainingCallbackActions


def create_add_exercise_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить упражнение", callback_data=CreateTrainingCallback(action=CreateTrainingCallbackActions.create_training)
    )
    builder.button(text='Сохранить', callback_data=CreateTrainingCallback(action=CreateTrainingCallbackActions.save))
    builder.button(text="Отмена", callback_data=CreateTrainingCallback(action=CreateTrainingCallbackActions.decline))
    return builder.as_markup()


class CreateTrainingKeyboard:
    def __init__(self, add_save_button):
        super().__init__()
