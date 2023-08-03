from aiogram import Router
from aiogram import F
from app.bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import UpstreamMenuMoveTo, CommonGoBackMoveTo
from app.workflows.common.utils.callback_properties.targets import ExerciseDbTargets
from app.workflows.common.utils.keyboards.exercise_db_choose import create_exercise_db_choose_keyboard
from ..utils.callback_properties.targets import ExerciseDbTargets
from app.entities.exercise.crud import *
from app.s3.downloader import create_presigned_url
from app.config import PHOTO_BUCKET


show_exercises_db_router = Router()


@show_exercises_db_router.callback_query(MoveToCallback.filter(F.move_to == UpstreamMenuMoveTo.show_exercise_db))
async def list_body_parts(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    body_parts = get_all_body_parts()
    await callback.message.edit_text(f'Давай выберем на какую часть тела хочешь просмотреть упражнения,'
                                     ' если частей тела нет то создай новое упражнение',
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=body_parts,
                                         source=callback,
                                         target=ExerciseDbTargets.show_body_part,
                                         go_back_filter=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu)))
    await callback.answer()


@show_exercises_db_router.callback_query(ChooseCallback.filter(F.target == ExerciseDbTargets.show_body_part))
async def show_muscle_groups(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    body_part = get_body_part_by_id(callback_data.option)
    await state.update_data({'body_part': str(body_part.id)})
    muscle_groups = get_muscle_groups_by_body_part(body_part=body_part)
    await callback.message.edit_text(f'Давай выберем на какую группу мышц хочешь просмотреть',
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=muscle_groups,
                                         source=callback,
                                         target=ExerciseDbTargets.show_muscle_group,
                                         go_back_filter=MoveToCallback(move_to=UpstreamMenuMoveTo.show_exercise_db)
                                     ))
    await callback.answer()


@show_exercises_db_router.callback_query(ChooseCallback.filter(F.target == ExerciseDbTargets.show_muscle_group))
async def show_exercises(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    muscle_group = get_muscle_group_by_id(callback_data.option)
    state_data = await state.get_data()
    go_back_ref = state_data['body_part']
    print(muscle_group)
    exercises = get_exercises_by_muscle_group(muscle_group=muscle_group)
    await state.update_data({'muscle_group': str(muscle_group.id)})
    print(exercises)
    if 'has_photo' in state_data.keys():
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f'Давай выберем упражнение',
                               reply_markup=create_exercise_db_choose_keyboard(
                                   options=exercises,
                                   source=callback,
                                   target=ExerciseDbTargets.show_exercise,
                                   go_back_filter=ChooseCallback(target=ExerciseDbTargets.show_body_part,
                                                                 option=go_back_ref)))
        await callback.message.delete()
    else:
        await callback.message.edit_text(f'Давай выберем упражнение',
                                         reply_markup=create_exercise_db_choose_keyboard(
                                             options=exercises,
                                             source=callback,
                                             target=ExerciseDbTargets.show_exercise,
                                             go_back_filter=ChooseCallback(target=ExerciseDbTargets.show_body_part,
                                                                           option=go_back_ref)))
        await callback.answer()



@show_exercises_db_router.callback_query(ChooseCallback.filter(F.target == ExerciseDbTargets.show_exercise))
async def show_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    exercise = get_exercise_by_id(callback_data.option)
    photo_link = create_presigned_url(PHOTO_BUCKET, exercise.photo_link)
    state_data = await state.get_data()
    go_back_ref = state_data['muscle_group']
    await state.update_data({'has_photo': True})
    print(state_data)
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                         caption=f"{exercise.name}",
                         reply_markup=create_exercise_db_choose_keyboard(
                             options=None,
                             source=callback,
                             target="optional",
                             go_back_filter=ChooseCallback(target=ExerciseDbTargets.show_muscle_group,
                                                           option=go_back_ref)))
    await callback.message.delete()







