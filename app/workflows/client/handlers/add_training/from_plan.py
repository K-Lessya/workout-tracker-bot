import logging, os, requests

from aiogram import Router
from aiogram.types import CallbackQuery, Message, FSInputFile, URLInputFile
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.workflows.client.classes.training import ClientTrainingSchema, ClientTrainingExerciseSchema
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, YesNoOptions
from app.callbacks.callbacks import MoveCallback
from app.utilities.helpers_functions import is_float
from app.workflows.client.utils.states import ClientStates
from app.bot import bot
import asyncio
from app.s3.uploader import upload_to_s3_and_update_progress
from app.keyboards.yes_no import YesNoKeyboard
from app.entities.single_file.models import Training, ClientTrainingExercise
from app.entities.single_file.crud import get_client_by_id
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo, ClientAddTrainingMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientAddTrainingTargets
from app.workflows.client.utils.keyboards.training_plan import PlanExerciseGoBackKeyboard
from app.workflows.client.utils.callback_properties.targets import ClientMyPlanTargets
from app.workflows.client.utils.keyboards.training_plan import TrainingDayExercises
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
# from moviepy.editor import VideoFileClip
from app.s3.downloader import create_presigned_url
from app.s3.uploader import upload_file
from app.config import PHOTO_BUCKET, MAX_FILE_SIZE
from app.keyboards.yes_no import YesNoKeyboard
from app.utilities.helpers_functions import callback_error_handler
from app.utilities.helpers_functions import album_handler
from app.translations.base_translations import translations

training_from_plan_router = Router()




@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.show_day))
@callback_error_handler
async def process_day(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(ClientStates.add_training.add_from_plan.show_day)
    client = get_client_by_id(tg_id=callback.from_user.id)
    lang = client.lang
    await state.update_data({'lang': lang})
    state_data = await state.get_data()
    training_days = state_data['training_days']
    print(training_days[int(callback_data.option)])
    selected_day = training_days[int(callback_data.option)]
    training = ClientTrainingSchema(selected_day.name)
    await state.update_data({'selected_day': int(callback_data.option), 'training': training})
    if callback.message.text:
        await callback.message.edit_text(translations[lang].client_add_from_plan_show_day.value
                                         .format(int(callback_data.option) + 1),
                                         reply_markup=TrainingDayExercises(selected_day.training_exercises,
                                              target=ClientAddTrainingTargets.show_exercise,
                                              go_back_target=ClientMainMenuMoveTo.add_training,
                                              lang=lang).as_markup())
    elif callback.message.photo or callback.message.video:
        await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id, text=translations[lang].client_add_from_plan_show_day
                               .value.format(int(callback_data.option) + 1),
                               reply_markup=TrainingDayExercises(selected_day.training_exercises,
                                                                 target=ClientAddTrainingTargets.show_exercise,
                                                                 go_back_target=ClientMainMenuMoveTo.add_training,
                                                                 lang=lang).as_markup())
    await callback.answer()

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.show_day)
async def handle_message(message: Message, state: FSMContext):
    await message.delete()

@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.show_exercise))
@callback_error_handler
async def process_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(ClientStates.add_training.add_from_plan.show_exercise)


    state_data = await state.get_data()
    training_days = state_data['training_days']
    lang = state_data['lang']
    training = state_data['training']
    selected_day = state_data['selected_day']
    selected_exercise = training_days[selected_day].training_exercises[int(callback_data.option)]
    training_exercise = ClientTrainingExerciseSchema(exercise=selected_exercise.exercise)
    if training_exercise.exercise not in [item.exercise for item in training.training_exercises]:
        training_exercise.add_runs(selected_exercise.num_runs)
        training_exercise.add_repeats(selected_exercise.num_repeats)
        selected_exercise_index = int(callback_data.option)
        await state.update_data({'selected_exercise_index': selected_exercise_index, 'training_exercise': training_exercise})
        await state.set_state(ClientStates.add_training.add_from_plan.process_exercise_weight)

        exercise = selected_exercise
        exercise_media_type = exercise.exercise.media_type
        await callback.message.edit_text(translations[lang].client_my_plan_loading_data.value)
        exercise_media_link = create_presigned_url(PHOTO_BUCKET, exercise.exercise.media_link)
        print(exercise_media_link)
        kwargs = {
            'chat_id': callback.from_user.id,
            'caption': translations[lang].client_add_from_plan_show_exercise
            .value.format(selected_exercise.exercise.name,
                          selected_exercise.num_runs,
                          selected_exercise.num_repeats,
                          selected_exercise.trainer_note),
            'reply_markup': PlanExerciseGoBackKeyboard(source_option=str(selected_day),
                                                       go_back_target=ClientAddTrainingTargets.show_day,
                                                       lang=lang).as_markup()
        }

        if exercise_media_type == 'photo':
            await state.update_data({'has_media': True})
            sent_message = await bot.send_photo(photo=exercise_media_link, **kwargs)
            await callback.message.delete()
        elif exercise_media_type == 'video':
            file = URLInputFile(url=exercise_media_link, bot=bot)
            sent_message = await bot.send_video(video=file, **kwargs)
            await callback.message.delete()
            pth_to_file=await bot.get_file(sent_message.video.file_id)
            print(pth_to_file.file_path)


        await state.update_data({'message_id_with_photo': sent_message.message_id})
        # await callback.answer('Загрузка завершена')
    else:
        await callback.answer(translations[lang].client_add_from_plan_show_exercise_already_added.value, show_alert=True)

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.process_exercise_weight)
async def process_exercise_weight(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    if is_float(message.text.replace(',','.')):
        callback_msg_id = state_data['message_id_with_photo']
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=callback_msg_id, reply_markup=None)
        training_days = state_data['training_days']
        selected_exercise_index = state_data['selected_exercise_index']
        training = state_data['training']
        print(training)
        selected_exercise = state_data['training_exercise']
        selected_day = state_data['selected_day']
        text = message.text.replace(",",".")

        selected_exercise.add_weight(float(text))
        await message.answer(text=translations[lang].client_add_from_plan_ask_video.value,
                             reply_markup=YesNoKeyboard(target=ClientAddTrainingTargets.process_video_link, lang=lang).as_markup())
    else:
        await message.answer(translations[lang].client_number_required.value)

@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.process_video_link))
@callback_error_handler
async def process_exercise_video_link(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    if callback_data.option == YesNoOptions.yes:
        await state.set_state(ClientStates.add_training.add_from_plan.process_exercise_video)
        await state.update_data({'multiple_files_message_sent': False, 'file_recieved': False})
        await callback.message.edit_text(translations[lang].client_add_from_plan_process_video.value)
    elif callback_data.option == YesNoOptions.no:
        selected_day_idx = state_data['selected_day']
        training_days = state_data['training_days']
        selected_day = training_days[selected_day_idx]
        training_exercise = state_data['training_exercise']
        training_exercise.add_video_link(video_link='')
        training_exercise.add_client_note(text='')
        await state.set_state(ClientStates.add_training.add_from_plan.show_day)
        current_training = state_data['training']
        current_training.add_exercise(training_exercise)
        reply_str = ''
        for exercise in current_training.training_exercises:
            reply_str+=f"{exercise.exercise.name}\n"
        keyboard = TrainingDayExercises(selected_day.training_exercises,
                                        target=ClientAddTrainingTargets.show_exercise,
                                        go_back_target=ClientMainMenuMoveTo.add_training,
                                        lang=lang)
        keyboard.button(text=translations[lang].client_training_save_btn.value,
                        callback_data=MoveCallback(target=ClientAddTrainingTargets.save_training).pack())
        await callback.message.edit_text(text=translations[lang].client_add_from_plan_ask_for_save.value.format(reply_str),
                                         reply_markup=keyboard.as_markup())

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.process_exercise_video)
@album_handler
async def process_exercise_video(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data["lang"]
    if message.video:
        video_id = message.video.file_id
        video_file = await bot.get_file(video_id)
        video_size = video_file.file_size
        if video_size <= MAX_FILE_SIZE:
            video_path = video_file.file_path

            print(video_path)


            training_exercise = state_data['training_exercise']
            path = f'tmp/{message.from_user.id}-from-plan-{training_exercise.exercise.name.replace(" ", "_")}.{video_path.split(".")[1]}'
            await bot.download_file(file_path=video_path, destination=path)
            training_exercise.add_video_link(path)
            training_days = state_data['training_days']
            selected_day_idx = state_data['selected_day']
            selected_day = training_days[selected_day_idx]
            training = state_data['training']
            await state.set_state(ClientStates.add_training.add_from_plan.ask_for_client_note)
            await message.answer(translations[lang].client_add_from_plan_ask_for_question.value,
                                 reply_markup=YesNoKeyboard(target=ClientAddTrainingTargets.process_client_note, lang=lang).as_markup())
        else:
            await message.answer(translations[lang].file_too_big.value)

    else:
        await message.answer(translations[lang].client_video_required.value)

@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.process_client_note))
@callback_error_handler
async def process_client_note_callback(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    training = state_data['training']
    training_exercise = state_data['training_exercise']
    selected_day_idx = state_data['selected_day']
    training_days = state_data['training_days']
    selected_day = training_days[selected_day_idx]
    if callback_data.option == YesNoOptions.yes:
        await state.set_state(ClientStates.add_training.add_from_plan.process_client_note)
        await callback.message.edit_text(translations[lang].client_add_from_plan_process_client_note.value)
    elif callback_data.option == YesNoOptions.no:
        training_exercise.add_client_note('')
        training.add_exercise(training_exercise)
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str+=f"{exercise.exercise.name}\n"
        keyboard = TrainingDayExercises(selected_day.training_exercises,
                                              target=ClientAddTrainingTargets.show_exercise,
                                              go_back_target=ClientMainMenuMoveTo.add_training,
                                        lang=lang)
        keyboard.button(text=translations[lang].client_training_save_btn.value, callback_data=MoveCallback(target=ClientAddTrainingTargets.save_training).pack())
        await callback.message.edit_text(text=translations[lang].client_add_from_plan_ask_for_save.value.format(reply_str),
                                         reply_markup=keyboard.as_markup())

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.process_client_note)
async def process_note(message: Message, state: FSMContext):
    note = message.text
    state_data = await state.get_data()
    lang = state_data.get('lang')
    training = state_data['training']
    training_exercise = state_data['training_exercise']
    selected_day_idx = state_data['selected_day']
    training_days = state_data['training_days']
    selected_day = training_days[selected_day_idx]
    training_exercise.add_client_note(text=note)
    training.add_exercise(training_exercise)
    reply_str = ''
    for exercise in training.training_exercises:
        reply_str += f"{exercise.exercise.name}\n"
    keyboard = TrainingDayExercises(selected_day.training_exercises,
                                    target=ClientAddTrainingTargets.show_exercise,
                                    go_back_target=ClientMainMenuMoveTo.add_training,
                                    lang=lang)
    keyboard.button(text=translations[lang].client_training_save_btn.value, callback_data=MoveCallback(target=ClientAddTrainingTargets.save_training).pack())
    await message.answer(text=translations[lang].client_add_from_plan_ask_for_save.value.format(reply_str),
                                     reply_markup=keyboard.as_markup())


@training_from_plan_router.callback_query(MoveCallback.filter(F.target == ClientAddTrainingTargets.save_training))
@callback_error_handler
async def process_save_training(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    training = state_data['training']
    mongo_training = Training(date=training.date, name=training.name)

    await callback.message.edit_text(translations[lang].client_add_from_plan_process_save.value)
    for exercise in training.training_exercises:
        await callback.message.edit_text(translations[lang].client_add_from_plan_process_sace_single_video
                                         .value.format(exercise.exercise.name))
        if exercise.video_link != '':
            s3_path = f'{callback.from_user.id}/trainings/{training.date}/{exercise.exercise.name.replace(" ", "_")}.{exercise.video_link.split(".")[1]}'
            logging.log(level=logging.INFO,msg=f'Processing video {s3_path}')
            # loop = asyncio.get_event_loop()

            # await upload_to_s3_and_update_progress(loop, exercise.video_link,s3_path,callback)
            upload_file(exercise.video_link, s3_path)
            os.remove(exercise.video_link)
            exercise.video_link = s3_path

        mongo_exercise = ClientTrainingExercise(exercise=exercise.exercise, num_runs=exercise.num_runs,
                                                num_repeats=exercise.num_repeats, video_link=exercise.video_link,
                                                weight=exercise.weight,
                                                client_note=exercise.client_note if exercise.client_note != ''
                                                else '')
        mongo_training.training_exercises.append(mongo_exercise)
    client = get_client_by_id(callback.from_user.id)
    client.trainings.append(mongo_training)
    client.save()
    if client.trainer:
        await callback.message.edit_text(translations[lang].ask_from_add_training_notification.value,
                                         reply_markup=YesNoKeyboard(
                                             target=ClientAddTrainingTargets.ask_send_notification,
                                             lang=lang).as_markup())
    else:
        await callback.message.edit_text(translations[lang].client_main_menu.value,
                                         reply_markup=create_client_main_menu_keyboard(client=client, lang=lang))















