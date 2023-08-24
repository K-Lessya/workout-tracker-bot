import logging
import os
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.workflows.client.classes.training import ClientTrainingSchema, ClientTrainingExerciseSchema
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, YesNoOptions
from app.callbacks.callbacks import MoveCallback
from app.utilities.helpers_functions import is_float
from app.workflows.client.utils.states import ClientStates
from app.bot import bot
from app.keyboards.yes_no import YesNoKeyboard
from app.entities.single_file.models import Training, ClientTrainingExercise
from app.entities.single_file.crud import get_client_by_id
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientAddTrainingTargets
from app.workflows.client.utils.keyboards.training_plan import PlanExerciseGoBackKeyboard
from app.workflows.client.utils.callback_properties.targets import ClientMyPlanTargets
from app.workflows.client.utils.keyboards.training_plan import TrainingDayExercises
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
# from moviepy.editor import VideoFileClip
from app.s3.downloader import create_presigned_url
from app.s3.uploader import upload_file
from app.config import PHOTO_BUCKET
from app.keyboards.yes_no import YesNoKeyboard


training_from_plan_router = Router()


@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.show_day))
async def process_day(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(ClientStates.add_training.add_from_plan.show_day)
    state_data = await state.get_data()
    training_days = state_data['training_days']
    print(training_days[int(callback_data.option)])
    selected_day = training_days[int(callback_data.option)]
    training = ClientTrainingSchema(selected_day.name)
    await state.update_data({'selected_day': int(callback_data.option), 'training': training})
    if callback.message.text:
        await callback.message.edit_text(
            f"Вот твои упражнения, для дня {int(callback_data.option) + 1}, если не знаешь как"
            f" выполнять просто выбери упражнение из списка",
            reply_markup=TrainingDayExercises(selected_day.training_exercises,
                                              target=ClientAddTrainingTargets.show_exercise,
                                              go_back_target=ClientMainMenuMoveTo.add_training).as_markup())
    elif callback.message.photo:
        await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id, text=f"Вот твои упражнения, для дня"
                                                                   f" {int(callback_data.option) + 1}, если не знаешь как"
                                                                   f" выполнять просто выбери упражнение из списка",
                               reply_markup=TrainingDayExercises(selected_day.training_exercises,
                                                                 target=ClientAddTrainingTargets.show_exercise,
                                                                 go_back_target=ClientMainMenuMoveTo.add_training).as_markup())

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.show_day)
async def handle_message(message: Message, state: FSMContext):
    await message.delete()


@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.show_exercise))
async def process_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(ClientStates.add_training.add_from_plan.show_exercise)
    state_data = await state.get_data()
    training_days = state_data['training_days']
    training = state_data['training']
    selected_day = state_data['selected_day']
    selected_exercise = training_days[selected_day].training_exercises[int(callback_data.option)]
    training_exercise = ClientTrainingExerciseSchema(exercise=selected_exercise.exercise)
    training_exercise.add_runs(selected_exercise.num_runs)
    training_exercise.add_repeats(selected_exercise.num_repeats)
    selected_exercise_index = int(callback_data.option)
    await state.update_data({'selected_exercise_index': selected_exercise_index, 'training_exercise': training_exercise})
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=selected_exercise.exercise.photo_link)
    await callback.message.delete()
    await callback.answer()
    await state.set_state(ClientStates.add_training.add_from_plan.process_exercise_weight)
    sent_message = await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                         caption=f'{selected_exercise.exercise.name}\n{selected_exercise.num_runs} подхода'
                                 f' по {selected_exercise.num_repeats} раз(а)\nВведи вес с которым работал',
                         reply_markup=PlanExerciseGoBackKeyboard(source_option=str(selected_day),
                                                                 go_back_target=ClientAddTrainingTargets.show_day).as_markup())
    await state.update_data({'message_id_with_photo': sent_message.message_id})

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.process_exercise_weight)
async def process_exercise_wight(message: Message, state: FSMContext):
    state_data = await state.get_data()
    callback_msg_id = state_data['message_id_with_photo']
    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=callback_msg_id, reply_markup=None)
    training_days = state_data['training_days']
    selected_exercise_index = state_data['selected_exercise_index']
    training = state_data['training']
    print(training)
    selected_exercise = state_data['training_exercise']
    selected_day = state_data['selected_day']
    text = message.text.replace(",",".")
    if is_float(text):
        selected_exercise.add_weight(float(text))
        await message.answer(text="Отлично, хочешь добавить видео?",
                             reply_markup=YesNoKeyboard(target=ClientAddTrainingTargets.process_video_link).as_markup())
    else:
        await message.answer("Нужно ввести число")


@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.process_video_link))
async def process_exercise_video_link(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == YesNoOptions.yes:
        await state.set_state(ClientStates.add_training.add_from_plan.process_exercise_video)
        await callback.message.edit_text("Присылай видео своего выполнения")
    elif callback_data.option == YesNoOptions.no:
        state_data = await state.get_data()
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
                                        go_back_target=ClientMainMenuMoveTo.add_training)
        keyboard.button(text="Cохранить",
                        callback_data=MoveCallback(target=ClientAddTrainingTargets.save_training).pack())
        await callback.message.edit_text(text="Ты добавил следующие упражнения из плана:\n"
                                              + reply_str
                                              + "Выбирай упражнение",
                                         reply_markup=keyboard.as_markup())

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.process_exercise_video)
async def process_exercise_video(message: Message, state: FSMContext):
    if message.video:
        video_id = message.video.file_id
        video_file = await bot.get_file(video_id)
        video_path = video_file.file_path

        print(video_path)
        state_data = await state.get_data()
        training_exercise = state_data['training_exercise']
        path = f'tmp/{message.from_user.id}-{video_path.split("/")[1]}'
        filename = path.split('.')[0]
        await bot.download_file(file_path=video_path, destination=path)
        training_exercise.add_video_link(path)
        training_days = state_data['training_days']
        selected_day_idx = state_data['selected_day']
        selected_day = training_days[selected_day_idx]
        training = state_data['training']
        await state.set_state(ClientStates.add_training.add_from_plan.ask_for_client_note)
        await message.answer("Хочешь оставить свой собственный коментарий или вопрос к видео для тренера?",
                             reply_markup=YesNoKeyboard(target=ClientAddTrainingTargets.process_client_note).as_markup())

    else:
        await message.answer('Необходимо прислать видео')


@training_from_plan_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.process_client_note))
async def process_client_note_callback(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    training = state_data['training']
    training_exercise = state_data['training_exercise']
    selected_day_idx = state_data['selected_day']
    training_days = state_data['training_days']
    selected_day = training_days[selected_day_idx]
    if callback_data.option == YesNoOptions.yes:
        await state.set_state(ClientStates.add_training.add_from_plan.process_client_note)
        await callback.message.edit_text('Напиши свой вопрос или комментарийц и тренер сможет его увидеть')
    elif callback_data.option == YesNoOptions.no:
        training_exercise.add_client_note('')
        training.add_exercise(training_exercise)
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str+=f"{exercise.exercise.name}\n"
        keyboard = TrainingDayExercises(selected_day.training_exercises,
                                              target=ClientAddTrainingTargets.show_exercise,
                                              go_back_target=ClientMainMenuMoveTo.add_training)
        keyboard.button(text="Cохранить", callback_data=MoveCallback(target=ClientAddTrainingTargets.save_training).pack())
        await callback.message.edit_text(text="Ты добавил следующие упражнения из плана:\n"
                                              + reply_str
                                              + "Выбирай упражнение",
                                         reply_markup=keyboard.as_markup())

@training_from_plan_router.message(ClientStates.add_training.add_from_plan.process_client_note)
async def process_note(message: Message, state: FSMContext):
    note = message.text
    state_data = await state.get_data()
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
                                    go_back_target=ClientMainMenuMoveTo.add_training)
    keyboard.button(text="Cохранить", callback_data=MoveCallback(target=ClientAddTrainingTargets.save_training).pack())
    await message.answer(text="Ты добавил следующие упражнения из плана:\n"
                                          + reply_str
                                          + "Выбирай упражнение",
                                     reply_markup=keyboard.as_markup())



@training_from_plan_router.callback_query(MoveCallback.filter(F.target == ClientAddTrainingTargets.save_training))
async def process_save_training(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    training = state_data['training']
    mongo_training = Training(date=training.date, name=training.name)

    for exercise in training.training_exercises:
        if exercise.video_link != '':
            s3_path = f'{callback.from_user.id}/trainings/{training.date}/{exercise.video_link.split("/")[1]}'
            logging.log(level=logging.INFO,msg=f'Processing video {s3_path}')
            upload_file(exercise.video_link, s3_path)
            os.remove(exercise.video_link)
            exercise.video_link = s3_path

        mongo_exercise = ClientTrainingExercise(exercise=exercise.exercise, num_runs=exercise.num_runs,
                                                num_repeats=exercise.num_repeats, video_link=exercise.video_link,
                                                weight=exercise.weight,
                                                client_note=exercise.client_note if exercise.client_note != ''
                                                else 'Отсутствует')
        mongo_training.training_exercises.append(mongo_exercise)
    client = get_client_by_id(callback.from_user.id)
    client.trainings.append(mongo_training)
    client.save()
    await callback.answer('Тренировка сохранена', show_alert=True, cache_time=300)

    await callback.message.edit_text("Меню клиента", reply_markup=create_client_main_menu_keyboard(client=client))















