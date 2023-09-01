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
from app.entities.exercise.crud import get_all_body_parts, get_body_part_by_id, get_muscle_groups_by_body_part, \
    get_exercises_by_muscle_group, get_exercise_by_id
from app.workflows.client.utils.callback_properties.targets import ClientAddCustomTrainingTargets
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo, ClientAddTrainingMoveTo
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.entities.single_file.models import Training, ClientTrainingExercise
from app.keyboards.yes_no import YesNoKeyboard
from app.utilities.default_callbacks.default_callbacks import YesNoOptions
from app.callbacks.callbacks import MoveCallback
from app.entities.exercise.exercise import ClientTrainingExercise
from app.utilities.helpers_functions import callback_error_handler
from app.utilities.helpers_functions import process_message_video
from app.entities.single_file.crud import get_client_by_id

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
    body_parts = get_all_body_parts()
    keyboard = ExerciseCommonListKeyboard(items=body_parts, tg_id=callback.from_user.id)
    keyboard.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=ClientMainMenuMoveTo.add_training).pack()))
    await callback.message.edit_text(f"Теперь давай выберем часть тела",
                         reply_markup=keyboard.as_markup())
    await callback.answer()

@custom_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddCustomTrainingTargets.choose_body_parts))
@callback_error_handler
async def choose_body_part(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    choosed_body_part = get_body_part_by_id(callback_data.option)
    muscle_groups = get_muscle_groups_by_body_part(choosed_body_part)
    await state.update_data({'choosed_body_part': choosed_body_part})
    keyboard = ExerciseCommonListKeyboard(items=muscle_groups, tg_id=callback.from_user.id)
    keyboard.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=ClientAddTrainingMoveTo.to_list_body_parts).pack()))
    await state.update_data({'choosed_body_part': choosed_body_part})
    await callback.message.edit_text('Теперь выбери на какую группу мышц будешь делать упражнение',
                                     reply_markup=keyboard.as_markup())


@custom_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddCustomTrainingTargets.choose_muscle_group))
@callback_error_handler
async def choose_body_part(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    choosed_body_part = state_data["choosed_body_part"]
    choosed_muscle_group = callback_data.option
    exercises = get_exercises_by_muscle_group(choosed_muscle_group)
    keyboard = ExerciseCommonListKeyboard(items=exercises, tg_id=callback.from_user.id)
    keyboard.row(InlineKeyboardButton(text="Назад",
                                      callback_data=ChooseCallback(target=ClientAddCustomTrainingTargets.choose_body_parts,
                                                                   option=str(choosed_body_part)).pack()))
    await state.update_data({'choosed_muscle_group': choosed_muscle_group})
    if callback.message.photo or callback.message.video:
        await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выбери упражнение',
                               reply_markup=keyboard.as_markup())
    else:
        await callback.message.edit_text('Выбери упражнение',
                                         reply_markup=keyboard.as_markup())

@custom_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddCustomTrainingTargets.choose_exercise))
@callback_error_handler
async def choose_body_part(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.edit_text("Загружаю упражнение")
    state_data = await state.get_data()
    choosed_muscle_group = state_data["choosed_muscle_group"]
    selected_exercise = get_exercise_by_id(callback_data.option)
    media_link = create_presigned_url(PHOTO_BUCKET, selected_exercise.media_link)
    await state.update_data({'choosed_exercise': choosed_muscle_group})
    kwargs = {
        'chat_id': callback.from_user.id,
        'caption': f'Введи количество подходов',
        'reply_markup': PlanExerciseGoBackKeyboard(source_option=str(choosed_muscle_group),
                                                   go_back_target=ClientAddCustomTrainingTargets.choose_muscle_group).as_markup()
    }
    if selected_exercise.media_type == "photo":
        await bot.send_photo(photo=media_link, **kwargs)
    elif selected_exercise.media_type == "video":
        file = URLInputFile(url=media_link, bot=bot)
        await bot.send_video(video=file, **kwargs)
    await state.update_data({'selected_exercise': selected_exercise})
    await state.set_state(ClientStates.add_training.add_custom.process_exercise_runs)
    await callback.message.delete()

@custom_training_router.message(ClientStates.add_training.add_custom.process_exercise_runs)
async def process_exercise_runs(message: Message, state: FSMContext):
    if message.text.isdigit():
        state_data = await state.get_data()
        new_exercise = ClientTrainingExerciseSchema(exercise=state_data["selected_exercise"])
        new_exercise.add_runs(int(message.text))
        await state.update_data({'new_exercise': new_exercise})
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
        body_parts = get_all_body_parts()
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str += f'{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}\n'

        keyboard = keyboard = ExerciseCommonListKeyboard(items=body_parts, tg_id=callback.from_user.id)
        keyboard.row(InlineKeyboardButton(text="Cохранить Тренировку",
                                          callback_data=MoveCallback(target=ClientAddCustomTrainingTargets.save_training).pack()))

        await callback.message.edit_text(text="Ты добавил следующие упражнения из плана:\n"
                                              + reply_str
                                              + "Выбирай следующее упражнение или сохрани тренировку",
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
        body_parts = get_all_body_parts()
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str += f'{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}\n'

        keyboard = keyboard = ExerciseCommonListKeyboard(items=body_parts, tg_id=callback.from_user.id)
        keyboard.row(InlineKeyboardButton(text="Cохранить Тренировку",
                                          callback_data=MoveCallback(
                                              target=ClientAddCustomTrainingTargets.save_training).pack()))

        await callback.message.edit_text(text="Ты добавил следующие упражнения из плана:\n"
                                              + reply_str
                                              + "Выбирай следующее упражнение или сохрани тренировку",
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
        body_parts = get_all_body_parts()
        reply_str = ''
        for exercise in training.training_exercises:
            reply_str += f'{exercise.exercise.name}, {exercise.num_runs}x{exercise.num_repeats}\n'

        keyboard = keyboard = ExerciseCommonListKeyboard(items=body_parts, tg_id=message.from_user.id)
        keyboard.row(InlineKeyboardButton(text="Cохранить Тренировку",
                                          callback_data=MoveCallback(
                                              target=ClientAddCustomTrainingTargets.save_training).pack()))

        await message.answer(text="Ты добавил следующие упражнения из плана:\n"
                                  + reply_str
                                  + "Выбирай следующее упражнение или сохрани тренировку",
                             reply_markup=keyboard.as_markup())


    @custom_training_router.callback_query(MoveCallback.filter(F.target == ClientAddCustomTrainingTargets.save_training))
    @callback_error_handler
    async def process_save_training(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
        state_data = await state.get_data()
        training = state_data['training']
        mongo_training = Training(name=training.name, date=training.date)

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













