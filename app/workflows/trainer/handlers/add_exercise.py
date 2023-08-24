from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.bot import bot
from app.utilities.default_callbacks.default_callbacks import ChooseCallback,MoveToCallback, YesNoOptions
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard

from ..utils.states import TrainerStates
from ..utils.callback_properties.targets import CreateExerciseTargets
from app.workflows.common.utils.keyboards.exercise_db_choose import create_exercise_db_choose_keyboard
from app.workflows.common.utils.callback_properties.targets import ExerciseDbTargets
from app.workflows.common.utils.callback_properties.movetos import ExerciseDbMoveTo, UpstreamMenuMoveTo,\
    CommonGoBackMoveTo
from app.s3.uploader import upload_file
from app.entities.exercise.crud import *
from app.utilities.helpers_functions import check_link
import os


add_exercise_router = Router()


@add_exercise_router.callback_query(MoveToCallback.filter(F.move_to == ExerciseDbMoveTo.create_exercise))
async def add_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.clear()
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_body_part_name)
    body_parts = get_all_body_parts()
    await callback.message.edit_text(f'Введи название части тела на которую делается '
                                     f'упражнение или выбери из существующих',
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=body_parts, source=callback,
                                         target=CreateExerciseTargets.process_body_part_name,
                                         go_back_filter=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu)
                                     ))


@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_body_part_name)
async def process_body_part_name_message(message: Message, state: FSMContext):
    await state.update_data({'body_part': message.text})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_muscle_group_name)
    await message.answer(f'Теперь введи группу мыщц для которой предназначено это упражнение')

@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.process_body_part_name))
async def process_body_part_name_callback(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    body_part = get_body_part_by_id(callback_data.option)
    muscle_groups = get_muscle_groups_by_body_part(body_part)
    await state.update_data({'body_part': body_part})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_muscle_group_name)
    await callback.message.edit_text(f'Теперь введи группу мыщц для которой предназначено это упражнение'
                                     f', или снова выбирай из списка',
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=muscle_groups, source=callback,
                                         target=CreateExerciseTargets.process_muscle_group_name,
                                         go_back_filter=MoveToCallback(
                                             move_to=CommonGoBackMoveTo.to_trainer_main_menu)))


@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_muscle_group_name)
async def process_muscle_group_name_message(message: Message, state: FSMContext):
    await state.update_data({'muscle_group': message.text})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_exercise_name)
    await message.answer(f'А теперь введи название упражнения')

@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.process_muscle_group_name))
async def process_muscle_group_name_callback(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    muscle_group = get_muscle_group_by_id(callback_data.option)
    await state.update_data({'muscle_group': muscle_group})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_exercise_name)
    await callback.message.edit_text(f'А теперь введи название упражнения')




@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_exercise_name)
async def process_muscle_group_name(message: Message, state: FSMContext):
    await state.update_data({'exercise_name': message.text})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_photo)
    await message.answer(f'Хочешь загрузить фотографию или видео с техникой упражнения?',
                         reply_markup=create_yes_no_keyboard(target=CreateExerciseTargets.ask_for_exercise_photo))


@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.ask_for_exercise_photo))
async def ask_for_photo(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    if callback_data.option == YesNoOptions.yes:
        await callback.message.edit_text(f'Тогда присылай фото или видео техники выполнения.\n'
                                         f'Желательно чтобы на фото были два крайних положения'
                                         f' при выполнении упражнения.')
        await callback.answer()
    elif callback_data.option == YesNoOptions.no:
        await state.update_data({'exercise_media_link': 'defaults/panda_workout.jpeg', 'exercise_media_type': 'photo'})
        await state.set_state(TrainerStates.exercises_db.add_exercise.process_save)
        await callback.message.edit_text(f'Давай все проверим.\nЧасть тела: {state_data["body_part"]}\nГруппа мышц:'
                                         f' {state_data["muscle_group"]}\nНазвание: {state_data["exercise_name"]}\n'
                                         f'Сохранить?',
                                         reply_markup=create_yes_no_keyboard(
                                             target=CreateExerciseTargets.process_save_exercise))


@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_photo)
async def process_media(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data({'exercise_media_type': 'photo'})
        file = await bot.get_file(message.photo[-1].file_id)
    elif message.video:
        await state.update_data({'exercise_media_type': 'video'})
        file = await bot.get_file(message.video.file_id)

    file_path = file.file_path
    destination = file_path.replace('/', '_')
    media_link = f'exercises/{file_path}'
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_save)
    await state.update_data({'local_path': f'tmp/{destination}', 'file_path': file_path, 'exercise_media_link': media_link})
    state_data = await state.get_data()
    await message.answer(f'Давай все проверим.\nЧасть тела: {state_data["body_part"]}\nГруппа мышц:'
                         f' {state_data["muscle_group"]}\nНазвание: {state_data["exercise_name"]}\n'
                         f'Сохранить?',
                         reply_markup=create_yes_no_keyboard(target=CreateExerciseTargets.process_save_exercise))



# @add_exercise_router.message(TrainerStates.exercises_db.add_exercise.ask_for_video)
# async def reply_from_question(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     last_bot_message = state_data['last_message']
#     await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=last_bot_message.message_id, reply_markup=None)
#     await bot.send_message(chat_id=message.from_user.id, text="Пожалуйста воспольщуйся кнопками", reply_markup=create_yes_no_keyboard(
#                              target=CreateExerciseTargets.process_exercise_video))


# @add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.process_exercise_video))
# async def process_video(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
#     if callback_data.option == YesNoOptions.yes:
#         await state.set_state(TrainerStates.exercises_db.add_exercise.process_video)
#         await callback.message.edit_text(f'Жду ссылку')
#         await callback.answer()
#
#     elif callback_data.option == YesNoOptions.no:
#         await state.update_data({'exercise_video_link': ''})
#
#         state_data = await state.get_data()
#


# @add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_video)
# async def process_video_link(message: Message, state: FSMContext):
#     check_link(link=message.text)
#     await state.update_data({'exercise_video_link': message.text})
#     state_data = await state.get_data()
#     await state.set_state(TrainerStates.exercises_db.add_exercise.process_save)
#     await message.answer(f'Давай все проверим.\nЧасть тела: {state_data["body_part"]}\nГруппа мышц:'
#                                      f' {state_data["muscle_group"]}\nНазвание: {state_data["exercise_name"]}\n'
#                                      f'Ссылка на видео: {state_data["exercise_video_link"]}'
#                                      f'Сохранить?',
#                                      reply_markup=create_yes_no_keyboard(
#                                          target=CreateExerciseTargets.process_save_exercise))


@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.process_save_exercise))
async def proces_save(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == YesNoOptions.yes:
        state_data = await state.get_data()
        await state.clear()

        if state_data['exercise_media_link'] != 'defaults/panda_workout.jpeg':
            await bot.download_file(file_path=state_data['file_path'], destination=state_data['local_path'])
            print('file_downloaded')

            upload_file(file=state_data['local_path'], destination=state_data['exercise_media_link'])
            os.remove(state_data['local_path'])
        if isinstance(state_data['body_part'], BodyPart):
            body_part = state_data['body_part']
        else:
            body_part = BodyPart(name=state_data['body_part'])
            create_body_part(body_part)
        if isinstance(state_data['muscle_group'], MuscleGroup):
            muscle_group = state_data['muscle_group']
        else:
            muscle_group = MuscleGroup(name=state_data['muscle_group'], body_part=body_part)
            create_muscle_group(muscle_group)
        exercise = Exercise(name=state_data['exercise_name'],
                            media_link=state_data['exercise_media_link'],
                            media_type=state_data['exercise_media_type'])

        exercise.muscle_groups.append(muscle_group)
        create_exercise(exercise)
        body_parts = get_all_body_parts()
        await callback.answer("Упражнение сохранено", show_alert=True)
        await callback.message.edit_text(f'Давай выберем упражнения',
                                         reply_markup=create_exercise_db_choose_keyboard(options=body_parts,
                                                                                         source=callback,
                                                                                         target=ExerciseDbTargets.show_body_part,
                                                                                         go_back_filter=MoveToCallback(
                                                                                             move_to=UpstreamMenuMoveTo.show_exercise_db)))
        await callback.answer()

    elif callback_data.option == YesNoOptions.no:
        await state.clear()
        body_parts = get_all_body_parts()
        await callback.message.edit_text(f'Упражнение не сохранено, возвращаемся в меню упражнений',
                                         reply_markup=create_exercise_db_choose_keyboard(options=body_parts,
                                                                                         source=callback,
                                                                                         target=ExerciseDbTargets.show_body_part,
                                                                                         go_back_filter=MoveToCallback(
                                                                                             move_to=UpstreamMenuMoveTo.show_exercise_db)
                                                                                         ))
        await callback.answer()
