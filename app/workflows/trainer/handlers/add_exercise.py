from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.bot import bot
from app.keyboards.yes_no import YesNoKeyboard
from app.utilities.default_callbacks.default_callbacks import ChooseCallback,MoveToCallback, YesNoOptions
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard
from app.s3.uploader import upload_to_s3_and_update_progress
from ..utils.keyboards.exercise_db import ExercisePlanListKeyboard
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
from app.utilities.helpers_functions import callback_error_handler
import asyncio
from app.config import MAX_FILE_SIZE
from app.entities.single_file.crud import get_trainer
from app.workflows.trainer.utils.classes.training_plan import PlanExercise
from app.utilities.helpers_functions import album_handler
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.keyboards.next_action import NextActionKeyboard
from app.translations.base_translations import translations

import threading

add_exercise_router = Router()

@add_exercise_router.callback_query(MoveToCallback.filter(F.move_to == ExerciseDbMoveTo.create_exercise))
@callback_error_handler
async def add_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_name = await state.get_state()
    state_data = await state.get_data()
    checker_state = "CreatePlan:process_body_parts"
    print('string state ' + str(state_name) )
    if str(state_name) == checker_state:
        print("MATCH!!!!!!")

        await state.update_data({"executing_from_plan": True})
    else:

        if not 'executing_from_plan' in state_data.keys():
            await state.clear()

    state_data = await state.get_data()
    if not 'executing_from_plan' in state_data.keys():
        go_back = CommonGoBackMoveTo.to_trainer_main_menu
    else:
        go_back = MyCLientsMoveTo.go_back_to_bodyparts_list

    print(state_data)
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_body_part_name)
    trainer = get_trainer(tg_id=callback.from_user.id)
    lang = trainer.lang
    await state.update_data({'lang': lang})
    body_parts = get_all_body_parts(trainer)
    await callback.message.edit_text(translations[lang].trainer_add_exercise_choose_body_part.value,
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=body_parts, source=callback,
                                         target=CreateExerciseTargets.process_body_part_name,
                                         go_back_filter=MoveToCallback(move_to=go_back),
                                         lang=lang
                                     ))
    await callback.answer()


@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_body_part_name)
async def process_body_part_name_message(message: Message, state: FSMContext):
    await state.update_data({'body_part': message.text})
    state_data = await state.get_data()
    lang = state_data.get('lang')
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_muscle_group_name)
    await message.answer(translations[lang].trainer_add_exercise_create_muscle_group_message.value)


@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.process_body_part_name))
@callback_error_handler
async def process_body_part_name_callback(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    body_part = get_body_part_by_id(callback_data.option)
    muscle_groups = get_muscle_groups_by_body_part(body_part)
    state_data = await state.get_data()
    lang = state_data['lang']
    await state.update_data({'body_part': body_part})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_muscle_group_name)
    await callback.message.edit_text(translations[lang].trainer_add_exercise_create_muscle_group_callback.value,
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=muscle_groups, source=callback,
                                         target=CreateExerciseTargets.process_muscle_group_name,
                                         go_back_filter=MoveToCallback(
                                             move_to=ExerciseDbMoveTo.create_exercise),
                                         lang=lang
                                     ))
    await callback.answer()


@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_muscle_group_name)
async def process_muscle_group_name_message(message: Message, state: FSMContext):
    await state.update_data({'muscle_group': message.text})
    state_data = await state.get_data()
    lang = state_data['lang']
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_exercise_name)
    await message.answer(translations[lang].trainer_add_exercise_type_exercise_name.value)
@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.process_muscle_group_name))
@callback_error_handler
async def process_muscle_group_name_callback(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    muscle_group = get_muscle_group_by_id(callback_data.option)
    await state.update_data({'muscle_group': muscle_group})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_exercise_name)
    state_data = await state.get_data()
    lang = state_data['lang']
    await callback.message.edit_text(translations[lang].trainer_add_exercise_type_exercise_name.value)
    await callback.answer()




@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_exercise_name)
async def process_muscle_group_name(message: Message, state: FSMContext):
    await state.update_data({'exercise_name': message.text, 'file_recieved': False})
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_photo)
    state_data = await state.get_data()
    lang = state_data['lang']
    await message.answer(translations[lang].trainer_add_exercise_ask_for_media.value,
                         reply_markup=YesNoKeyboard(target=CreateExerciseTargets.ask_for_exercise_photo, lang=lang).as_markup())


@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.ask_for_exercise_photo))
@callback_error_handler
async def ask_for_photo(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    if callback_data.option == YesNoOptions.yes:
        await state.update_data({'multiple_files_message_sent': False})
        await callback.message.edit_text(translations[lang].trainer_add_exercise_process_media.value)
    elif callback_data.option == YesNoOptions.no:
        await state.update_data({'exercise_media_link': 'defaults/panda_workout.jpeg', 'exercise_media_type': 'photo'})
        await state.set_state(TrainerStates.exercises_db.add_exercise.process_save)
        if isinstance(state_data["body_part"], BodyPart):
            body_part_name = state_data['body_part'].name
        else:
            body_part_name = state_data['body_part']
        if isinstance(state_data['muscle_group'], MuscleGroup):
            muscle_group_name = state_data["muscle_group"].name
        else:
            muscle_group_name = state_data['muscle_group']
        await callback.message.edit_text(translations[lang].trainer_add_exercise_ask_for_save.value.format(
            body_part_name,
            muscle_group_name,
            state_data["exercise_name"]
        ),
        reply_markup=YesNoKeyboard(target=CreateExerciseTargets.process_save_exercise, lang=lang).as_markup())
    await callback.answer()


@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.process_photo)
@album_handler
async def process_media(message: Message | list[Message], state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    if message.photo or message.video:
        await state.set_state(TrainerStates.exercises_db.add_exercise.process_save)
        await state.update_data({"file_recieved": True})
        if isinstance(message, Message):
            if message.photo:
                await state.update_data({'exercise_media_type': 'photo'})
                file = await bot.get_file(message.photo[-1].file_id)
            elif message.video:
                await state.update_data({'exercise_media_type': 'video'})
                file = await bot.get_file(message.video.file_id)

        if file.file_size <= MAX_FILE_SIZE:

            file_path = file.file_path
            destination = file_path.replace('/', '_')
            media_link = f'exercises/{file_path}'

            await state.update_data(
                {'local_path': f'tmp/{destination}', 'file_path': file_path, 'exercise_media_link': media_link})
            state_data = await state.get_data()
            if isinstance(state_data["body_part"], BodyPart):
                body_part_name = state_data['body_part'].name
            else:
                body_part_name = state_data['body_part']
            if isinstance(state_data['muscle_group'], MuscleGroup):
                muscle_group_name = state_data["muscle_group"].name
            else:
                muscle_group_name = state_data['muscle_group']
            await message.answer(
                translations[lang].trainer_add_exercise_ask_for_save.value.format(
                    body_part_name,
                    muscle_group_name,
                    state_data["exercise_name"]
                ),
                reply_markup=YesNoKeyboard(target=CreateExerciseTargets.process_save_exercise, lang=lang).as_markup()
            )
        else:
            await message.answer(translations[lang].trainer_add_exercise_process_media_file_size_alert.value)
    else:
        await message.answer(translations[lang].trainer_add_exercise_process_media_text_recieved.value)


@add_exercise_router.message(TrainerStates.exercises_db.add_exercise.ask_for_video)
async def reply_from_question(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    last_bot_message = state_data['last_message']
    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=last_bot_message.message_id, reply_markup=None)
    await bot.send_message(chat_id=message.from_user.id,
                           text=translations[lang].use_btn_alert, reply_markup=create_yes_no_keyboard(
                             target=CreateExerciseTargets.process_exercise_video))


@add_exercise_router.callback_query(ChooseCallback.filter(F.target == CreateExerciseTargets.process_save_exercise))
@callback_error_handler
async def proces_save(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    if callback_data.option == YesNoOptions.yes:
        state_data = await state.get_data()
        if "executing_from_plan" in state_data.keys():
            print(len(state_data['plan'].days))
        else:
            await state.clear()

        if state_data['exercise_media_link'] != 'defaults/panda_workout.jpeg':
            await callback.message.edit_text(translations[lang].trainer_add_exercise_process_save_process_file.value)
            file_size = await bot.download_file(file_path=state_data['file_path'], destination=state_data['local_path'])



            progress_message = await callback.message.edit_text(
                translations[lang].trainer_add_exercise_process_save_upload_file.value
            )

            print('file_downloaded')

            upload_file(file=state_data['local_path'],
                        destination=state_data['exercise_media_link']
                        )
            await callback.message.edit_text(translations[lang].trainer_add_exercise_process_save_file_uploaded.value)
            os.remove(state_data['local_path'])
            await callback.message.edit_text(translations[lang].trainer_add_exercise_process_save_process_bp_mg.value)

        if isinstance(state_data['body_part'], BodyPart):
            body_part = state_data['body_part']
        else:
            body_part = BodyPart(name=state_data['body_part'], trainer=trainer)
            create_body_part(body_part)
        if isinstance(state_data['muscle_group'], MuscleGroup):
            muscle_group = state_data['muscle_group']
        else:
            muscle_group = MuscleGroup(name=state_data['muscle_group'], body_part=body_part)
            create_muscle_group(muscle_group)
        await callback.message.edit_text(translations[lang].trainer_add_exercise_process_save_loading.value)

        exercise = Exercise(name=state_data['exercise_name'],
                            media_link=state_data['exercise_media_link'],
                            media_type=state_data['exercise_media_type'],
                            trainer=trainer)

        exercise.muscle_groups.append(muscle_group)
        create_exercise(exercise)
        body_parts = get_all_body_parts(trainer)
        print(state_data)
        if 'executing_from_plan' in state_data.keys():
            plan_exercise = PlanExercise(exercise=exercise)
            state_data['plan'].days[-1].add_exercise(plan_exercise)
            await state.set_state(TrainerStates.my_clients.create_plan.process_trainer_note)

            message_with_button = await callback.message.answer(translations[lang].trainer_create_plan_add_trainer_note.value,
                                          reply_markup=NextActionKeyboard(target=MyCLientsMoveTo.skip_trainer_note,
                                                                          lang=lang).as_markup())
            await state.update_data({"to_delete_keyboard": message_with_button})
            await callback.message.delete()
        else:

            await callback.message.answer(translations[lang].trainer_exercise_db_choose_bodypart.value,
                                             reply_markup=create_exercise_db_choose_keyboard(options=body_parts,
                                                                                             source=callback,
                                                                                             target=ExerciseDbTargets.show_body_part,
                                                                                             go_back_filter=MoveToCallback(
                                                                                                 move_to=UpstreamMenuMoveTo.show_exercise_db),
                                                                                             lang=lang
                                                                                             ))
            await callback.message.delete()

    elif callback_data.option == YesNoOptions.no:

        body_parts = get_all_body_parts(trainer)
        state_data = await state.get_data()
        if 'executing_from_plan' in state_data.keys():
            await callback.answer(translations[lang].trainer_add_exercise_process_save_not_saved.value, show_alert=True)
            plan = state_data['plan']
            current_day = plan.days[-1]
            await callback.message.answer(translations[lang].trainer_create_plan_choose_exercise_for_day.value.format(len(plan.days)),
                                          reply_markup=ExercisePlanListKeyboard(items=body_parts,
                                                                                tg_id=callback.from_user.id,
                                                                                day_num=len(plan.days),
                                                                                exercises_length=len(
                                                                                    current_day.exercises)).as_markup())
        else:
            await state.clear()
            await callback.message.answer(translations[lang].trainer_add_exercise_process_save_not_saved.value,
                                             reply_markup=create_exercise_db_choose_keyboard(options=body_parts,
                                                                                         source=callback,
                                                                                         target=ExerciseDbTargets.show_body_part,
                                                                             go_back_filter=MoveToCallback(
                                                                                             move_to=UpstreamMenuMoveTo.show_exercise_db),
                                                                                             lang=lang
                                                                                         ))
        await callback.message.delete()
        await callback.answer()
