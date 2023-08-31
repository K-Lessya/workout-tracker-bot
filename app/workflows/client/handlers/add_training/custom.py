from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.workflows.client.utils.states import ClientStates
from app.workflows.client.classes.training import ClientTrainingSchema, ClientTrainingExerciseSchema
from app.workflows.common.utils.keyboards.exercise_db_choose import ExerciseCommonListKeyboard
from app.entities.exercise.crud import get_all_body_parts, get_body_part_by_id, get_muscle_groups_by_body_part
from app.workflows.client.utils.callback_properties.targets import  ClientAddCustomTrainingTargets
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo, ClientAddTrainingMoveTo
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.callbacks.callbacks import MoveCallback
from app.utilities.helpers_functions import callback_error_handler

custom_training_router = Router()



@custom_training_router.message(ClientStates.add_training.add_custom.process_training_name)
async def process_training_name(message: Message, state: FSMContext):
    training = ClientTrainingSchema(text=message.text)
    body_parts = get_all_body_parts()
    keyboard = ExerciseCommonListKeyboard(items=body_parts, tg_id=message.from_user.id)
    keyboard.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=ClientMainMenuMoveTo.add_training).pack()))
    await state.update_data({'training': training})
    await state.set_state(ClientStates.add_training.add_custom.process_buttons)
    await message.answer(f"Теперь давай выберем часть тела",
                         reply_markup=keyboard.as_markup())

@custom_training_router.callback_query(MoveCallback.filter(F.target == ClientAddTrainingMoveTo.to_list_body_parts))
@callback_error_handler
async def list_body_parts(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    await callback.answer()

@custom_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddCustomTrainingTargets.show_body_parts))
@callback_error_handler
async def choose_body_part(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    choosed_body_part = get_body_part_by_id(callback_data.option)
    muscle_groups = get_muscle_groups_by_body_part(choosed_body_part)
    keyboard = ExerciseCommonListKeyboard(items=muscle_groups, tg_id=callback.from_user.id)
    keyboard.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=ClientMainMenuMoveTo.add_training).pack()))
    await state.update_data({'choosed_body_part': choosed_body_part})
    await callback.message.edit_text('Теперь выбери на какую группу мышц будешь делать упражнение',
                                     reply_markup=ExerciseCommonListKeyboard(items=muscle_groups,
                                                                             tg_id=callback.from_user.id))

