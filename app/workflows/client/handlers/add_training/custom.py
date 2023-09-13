import os

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, URLInputFile
from aiogram.fsm.context import FSMContext
from app.bot import bot
from app.s3.downloader import create_presigned_url
from app.s3.uploader import upload_file
from app.config import PHOTO_BUCKET
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.client.utils.keyboards.training_plan import PlanExerciseGoBackKeyboard
from app.workflows.client.utils.states import ClientStates
from app.workflows.client.classes.training import ClientTrainingSchema, ClientTrainingExerciseSchema
from app.workflows.common.utils.keyboards.exercise_db_choose import ExerciseCommonListKeyboard
from app.entities.exercise.crud import get_all_body_parts
from app.workflows.client.utils.callback_properties.targets import ClientAddCustomTrainingTargets
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.entities.single_file.models import Training
from app.keyboards.yes_no import YesNoKeyboard
from app.utilities.default_callbacks.default_callbacks import YesNoOptions
from app.callbacks.callbacks import MoveCallback
from app.utilities.helpers_functions import callback_error_handler
from app.utilities.helpers_functions import process_message_video
from app.entities.single_file.crud import get_client_by_id
from app.entities.exercise.exercise import Exercise, ClientTrainingExercise
from app.entities.exercise.crud import get_client_exercises, get_exercise_by_id

custom_training_router = Router()



@custom_training_router.message(ClientStates.add_training.add_custom.process_training_name)
async def process_training_name(message: Message, state: FSMContext):
    training = ClientTrainingSchema(text=message.text)
    await state.update_data({'training': training})
    await state.set_state(ClientStates.add_training.add_custom.process_exercise_name)
    client = get_client_by_id(message.from_user.id)
    client_exercises = client.custom_exercises
    keyboard = ExerciseCommonListKeyboard(items=client_exercises, tg_id=message.from_user.id)

    await message.answer(f"Теперь давай введем название первого упражнения или выбери из уже созданных тобой упражнений",
                         reply_markup=keyboard.as_markup())


@custom_training_router.message(ClientStates.add_training.add_custom.process_exercise_name)
async def process_exercise_name(message: Message, state: FSMContext):
    exercise_name = message.text
    client = get_client_by_id(message.from_user.id)
    exercise = ClientTrainingExerciseSchema(exercise=Exercise(name=exercise_name,
                                                              media_type='photo',
                                                              media_link='defaults/panda_workout.jpeg'))
    exercise.exercise.save()
    client.custom_exercises.append(exercise.exercise)
    client.save()
    await state.update_data({'new_exercise': exercise, 'client': client})
    await state.set_state(ClientStates.add_training.add_custom.process_exercise_runs)
    await message.answer("А теперь введи количество подходов")



@custom_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddCustomTrainingTargets.choose_exercise))
async def process_chosed_exercise_runs(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    exercise_id = callback_data.option
    exercise = ClientTrainingExerciseSchema(exercise=get_exercise_by_id(exercise_id))
    state_data = await state.get_data()
    training = state_data['training']
    if exercise.exercise in [item.exercise for item in training.training_exercises]:
        await callback.answer("Ты уже добавил это упражнение в тренировку, выбери дрпугое или создай новое", show_alert=True)

    else:
        client = get_client_by_id(callback.from_user.id)
        await state.update_data({'new_exercise': exercise, 'client': client})
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_runs)
        await callback.message.edit_text("А теперь введи количество подходов")



@custom_training_router.message(ClientStates.add_training.add_custom.process_exercise_runs)
async def process_exercise_runs(message: Message, state: FSMContext):
    if message.text.isdigit():
        state_data = await state.get_data()
        exercise = state_data['new_exercise']
        exercise.add_runs(int(message.text))
        await state.update_data({'new_exercise': exercise})
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_repeats)
        await message.answer("Хорошо, а теперь введи количество повторений за подход")
    else:
        await message.answer("Нужно ввести число")

@custom_training_router.message(ClientStates.add_training.add_custom.process_exercise_repeats)
async def process_exercise_runs(message: Message, state: FSMContext):
    if message.text.isdigit():
        state_data = await state.get_data()
        new_exercise = state_data['new_exercise']
        new_exercise.add_repeats(int(message.text))
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_weight)
        await message.answer("Хорошо, а теперь введи вес с которым работал")
    else:
        await message.answer("Нужно ввести число")

@custom_training_router.message(ClientStates.add_training.add_custom.process_exercise_weight)
async def process_exercise_runs(message: Message, state: FSMContext):
    if message.text.isdigit():
        state_data = await state.get_data()
        new_exercise = state_data['new_exercise']
        new_exercise.add_weight(int(message.text))
        await state.set_state(ClientStates.add_training.add_custom.process_buttons)
        await message.answer("Хочешь загрузить свое видео выполнения чтобы тренер мог его посмотреть?",
                             reply_markup=YesNoKeyboard(
                                 target=ClientAddCustomTrainingTargets.ask_for_exercise_video).as_markup())
    else:
        await message.answer("Нужно ввести число")


@custom_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddCustomTrainingTargets.ask_for_exercise_video))
@callback_error_handler
async def process_exercise_video_answer(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == YesNoOptions.yes:
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_video)
        await callback.message.edit_text('Присылай видео своего выполнения')
    elif callback_data.option == YesNoOptions.no:
        state_data = await state.get_data()
        new_exercise = state_data['new_exercise']
        new_exercise.add_video_link('')
        new_exercise.add_client_note('')
        training = state_data['training']
        training.training_exercises.append(new_exercise)
        await state.set_state(ClientStates.add_training.add_custom.process_buttons)
        client = state_data['client']
        exercises = client.custom_exercises
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str += f'{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}\n'

        keyboard = ExerciseCommonListKeyboard(items=exercises, tg_id=callback.from_user.id)
        keyboard.row(InlineKeyboardButton(text="Cохранить Тренировку",
                                          callback_data=MoveCallback(target=ClientAddCustomTrainingTargets.save_training).pack()))
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_name)
        await callback.message.edit_text(text="Ты добавил следующие упражнения из плана:\n"
                                              + reply_str
                                              + "Вводи название следующего упражнения или сохрани тренировку",
                                         reply_markup=keyboard.as_markup())


@custom_training_router.message(ClientStates.add_training.add_custom.process_exercise_video)
async def process_client_exercise_video(message: Message, state: FSMContext):
    if message.video:
        file_path = await process_message_video(message)
        state_data = await state.get_data()
        new_exercise = state_data['new_exercise']
        new_exercise.add_video_link(file_path)
        await state.set_state(ClientStates.add_training.add_custom.process_buttons)
        await message.answer("Отлично, хочешь добавить комментарий с вопросом по твоему видео,"
                             " чтобы тренер мог лучше понять как комментировать технику?",
                             reply_markup=YesNoKeyboard(
                                 target=ClientAddCustomTrainingTargets.ask_for_exercise_comment).as_markup())
    else:
        await message.answer("Я ожидаю видео")

@custom_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddCustomTrainingTargets.ask_for_exercise_comment))
@callback_error_handler
async def process_client_note_answer(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == YesNoOptions.yes:
        await state.set_state(ClientStates.add_training.add_custom.process_client_comment)
        await callback.message.edit_text('Напиши свой комментарий')

    else:
        state_data = await state.get_data()
        new_exercise = state_data['new_exercise']
        new_exercise.add_client_note('')
        training = state_data['training']
        training.training_exercises.append(new_exercise)
        await state.set_state(ClientStates.add_training.add_custom.process_buttons)
        client = state_data['client']
        exercises = client.custom_exercises
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str += f'{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}\n'

        keyboard = ExerciseCommonListKeyboard(items=exercises, tg_id=callback.from_user.id)
        keyboard.row(InlineKeyboardButton(text="Cохранить Тренировку",
                                          callback_data=MoveCallback(
                                              target=ClientAddCustomTrainingTargets.save_training).pack()))
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_name)
        await callback.message.edit_text(text="Ты добавил следующие упражнения из плана:\n"
                                              + reply_str
                                              + "Вводи название следующего упражнения или сохрани тренировку",
                                         reply_markup=keyboard.as_markup())

@custom_training_router.message(ClientStates.add_training.add_custom.process_client_comment)
async def process_client_note(message: Message, state: FSMContext):
    if message.text:
        client_note = message.text
        state_data = await state.get_data()
        new_exercise = state_data['new_exercise']
        new_exercise.add_client_note(client_note)
        training = state_data['training']
        training.training_exercises.append(new_exercise)
        await state.set_state(ClientStates.add_training.add_custom.process_buttons)
        client = state_data['client']
        exercises = client.custom_exercises
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str += f'{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}\n'

        keyboard = keyboard = ExerciseCommonListKeyboard(items=exercises, tg_id=message.from_user.id)
        keyboard.row(InlineKeyboardButton(text="Cохранить Тренировку",
                                          callback_data=MoveCallback(
                                              target=ClientAddCustomTrainingTargets.save_training).pack()))
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_name)
        await message.answer(text="Ты добавил следующие упражнения из плана:\n"
                                  + reply_str
                                  + "Вводи название следующего упражнения или сохрани тренировку",
                             reply_markup=keyboard.as_markup())


@custom_training_router.callback_query(MoveCallback.filter(F.target == ClientAddCustomTrainingTargets.save_training))
@callback_error_handler
async def process_save_training(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    training = state_data['training']
    mongo_training = Training(name=training.name, date=training.date)
    client = state_data['client']

    for idx ,exercise in enumerate(training.training_exercises):
        if exercise.video_link != '':
            await callback.message.edit_text(f"Сохраняю видео для упражнения {idx+1}: {exercise.exercise.name}")
            s3_destination = f'{callback.from_user.id}/trainings/{training.date}/{exercise.video_link.split("_")[1]}'
            local_path = exercise.video_link
            upload_file(local_path, s3_destination)
            os.remove(local_path)
            exercise.video_link = s3_destination

        mongo_exercise = ClientTrainingExercise(
            exercise=exercise.exercise,
            weight=exercise.weight,
            num_runs=exercise.num_runs,
            num_repeats=exercise.num_repeats,
            video_link=exercise.video_link,
            client_note=exercise.client_note
        )
        mongo_training.training_exercises.append(mongo_exercise)


    client = get_client_by_id(tg_id=callback.from_user.id)
    client.trainings.append(mongo_training)
    client.save()

    await callback.message.edit_text("Меню клиента", reply_markup=create_client_main_menu_keyboard(client))













