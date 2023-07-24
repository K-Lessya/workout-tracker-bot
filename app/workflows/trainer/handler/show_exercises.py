from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.utilities.default_callbacks.choose_callback import ChooseCallback, YesNoOptions
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard
from ..utils.states import TrainerStates
from ..utils.callback_properties import TrainerMainMenuTargets
from ..utils.keyboards.body_parts import create_show_body_parts_keyboard
from ..utils.callback_properties import ListBodyPartsOptions, ListBodyPartsTargets, CreateExerciseTargets
from app.entities.exercise.exercise import Exercise, MuscleGroup, BodyPart
from app.entities.exercise.crud import *


show_exercises_router = Router()


@show_exercises_router.callback_query(ChooseCallback.filter(F.target == TrainerMainMenuTargets.list_exercises))
async def list_body_parts(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    body_parts = get_all_body_parts()
    await callback.message.edit_text(f'Давай выберем на какую часть тела хочешь просмотреть упражнения,'
                                     ' если частей тела нет то создай новое упражнение',
                                     reply_markup=create_show_body_parts_keyboard(body_parts=body_parts))
    await callback.answer()



