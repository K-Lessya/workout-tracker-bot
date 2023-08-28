import os
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext

from app.utilities.default_callbacks.default_callbacks import ChooseCallback, YesNoOptions, MoveToCallback
from app.workflows.client.utils.callback_property import CreateTrainingCallback, CreateTrainingCallbackActions, ClientMainMenuTargets,\
    ClientMainMenuOptions, ClientExerciseTargets

from app.workflows.client.utils.states import ClientStates
from app.bot import bot
from app.workflows.client.utils.keyboards.training import TrainingTypeKeyboard
from app.entities.single_file.models import Training, ClientTrainingExercise
from app.entities.single_file.crud import create_training, get_client_by_id
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.client.utils.keyboards.create_trainings import create_add_exercise_keyboard
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard
from app.s3.uploader import upload_file
from datetime import date
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientAddTrainingTargets
from app.workflows.client.utils.callback_properties.options import ClientAddTrainingOptions
from app.entities.training_plan.crud import get_training_days
from app.workflows.client.utils.keyboards.training_plan import TrainingDaysKeyboard
from app.workflows.client.handlers.add_training.from_plan import training_from_plan_router
from app.callbacks.callbacks import MoveCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.utilities.helpers_functions import callback_error_handler
add_training_router = Router()
add_training_router.include_routers(training_from_plan_router)

@add_training_router.callback_query(MoveCallback.filter(F.target == ClientMainMenuMoveTo.add_training))
@callback_error_handler# Create training flow
async def start_creating_training(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    await state.set_state(ClientStates.add_training.process_training_type)

    await callback.message.edit_text(f"Хочешь добавить собственную тренировку или из плана",
                                     reply_markup=TrainingTypeKeyboard().as_markup())
@add_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.choose_training_type))
@callback_error_handler
async def process_training_type(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    training = Training(date=date.today())
    await state.update_data({'training': training})
    if callback_data.option == ClientAddTrainingOptions.custom:
        await state.set_state(ClientStates.add_training.add_custom.process_exercise_name)
        await callback.message.edit_text(f'Начнем с добавления твоего первого упражнения.\nВыбирай из категорий',
                                     reply_markup=create_add_exercise_keyboard())
    elif callback_data.option == ClientAddTrainingOptions.from_plan:
        training_days = get_training_days(client_id=callback.from_user.id)
        if training_days:
            await state.update_data({"training_days": training_days})
            await state.set_state(ClientStates.add_training.add_from_plan.show_plan)
            await callback.message.edit_text(f'Выбери день из плана',
                                             reply_markup=TrainingDaysKeyboard(training_days,
                                                                               target=ClientAddTrainingTargets.show_day,
                                                                               go_back_target=CommonGoBackMoveTo.to_client_main_menu).as_markup())
        else:
            await callback.answer("Тренер еще не составил для тебя план", show_alert=True)










# @add_training_router.message(ClientStates.process_training_name)
# async def process_training_name(message: Message, state: FSMContext):
#
#     # create_training(tg_id=message.from_user.id, training=training)
#     await state.update_data({'training': training})
#     await message.answer(f'Начнем с добавления твоего первого упражнения.\nЖми кнопку, не стесняйся',
#                                      reply_markup=create_add_exercise_keyboard())
#
# @add_training_router.callback_query(CreateTrainingCallback.filter(F.action == CreateTrainingCallbackActions.create_training))
#@callback_error_handler
# async def process_exercise(callback: CallbackQuery, callback_data: CreateTrainingCallback, state: FSMContext):
#     await state.set_state(ClientStates.process_exercise_name)
#     await callback.message.edit_text(f'Введи название упражнения')
#     await callback.answer()
#
#
# @add_training_router.message(ClientStates.process_exercise_name)
# async def process_exercise_name(message: Message, state: FSMContext):
#     await state.update_data({'exercise': {'name': message.text}})
#     await state.set_state(ClientStates.process_exercise_runs)
#     await message.answer(f'Отлично, теперь запиши количество подходов')
#
#
# @add_training_router.message(ClientStates.process_exercise_runs)
# async def process_exercise_name(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     state_data['exercise']['runs'] = message.text
#     await state.update_data(state_data)
#     await state.set_state(ClientStates.process_exercise_repeats)
#     await message.answer(f'Отлично, теперь запиши количество потворений за подход')
#
#
# @add_training_router.message(ClientStates.process_exercise_repeats)
# async def process_exercise_name(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     state_data['exercise']['repeats'] = message.text
#     await state.update_data(state_data)
#     await state.set_state(ClientStates.process_exercise_weight)
#     await message.answer(f'Отлично, теперь запиши рабочий вес')
#
# @add_training_router.message(ClientStates.process_exercise_weight)
# async def process_exercise_name(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     state_data['exercise']['weight'] = message.text
#     await state.update_data(state_data)
#     await state.set_state(ClientStates.process_exercise_video)
#     await message.answer(f'Супер, желаешь прикрепить видео выполнения?',
#                          reply_markup=create_yes_no_keyboard(target=ClientExerciseTargets.attach_video))
#
# @add_training_router.callback_query(ChooseCallback.filter(F.target == ClientExerciseTargets.attach_video),
#@callback_error_handler
#                               ChooseCallback.filter(F.option == YesNoOptions.yes))
# async def send_video_message(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
#     await callback.message.edit_text(f'Пришли мне видео выполнения упражнения')
#     await callback.answer()
#
# @add_training_router.callback_query(ChooseCallback.filter(F.target == ClientExerciseTargets.attach_video),
#@callback_error_handler
#                               ChooseCallback.filter(F.option == YesNoOptions.no))
# async def no_process_video(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
#     state_data = await state.get_data()
#     state_data['exercise']['video_link'] = None
#
#     await state.update_data(state_data)
#     exercise = state_data['exercise']
#     state_data.pop('exercise')
#     state_data['training'].training_exercises.append(ClientTrainingExercise(name=exercise['name'],
#                                                                             num_runs=exercise['runs'],
#                                                                             num_repeats=exercise['repeats'],
#                                                                             weight=exercise['weight'],
#                                                                             video_link=exercise['video_link']))
#     await callback.message.edit_text('Учти, без видео тренер не сможет дать комментарий, желаешь добавить еще одно упражнение?',
#                                      reply_markup=create_add_exercise_keyboard())
#
#
# @add_training_router.message(ClientStates.process_exercise_video)
# async def process_video(message: Message, state: FSMContext):
#     destination = f'tmp/{message.video.file_id}.mp4'
#
#     file = await bot.get_file(message.video.file_id)
#     await message.answer(f'Загружаю видео, это может занять несколько секунд...')
#     await bot.download_file(file.file_path, destination)
#     upload_file(file=destination, destination=f'users/{message.from_user.id}/{message.video.file_id}.mp4')
#     os.remove(destination)
#
#     state_data = await state.get_data()
#     state_data['exercise']['video_link'] = f'users/{message.from_user.id}/{message.video.file_id}.mp4'
#     await state.update_data(state_data)
#     state_data = await state.get_data()
#     exercise = state_data['exercise']
#     state_data.pop('exercise')
#
#     state_data['training'].training_exercises.append(ClientTrainingExercise(name=exercise['name'],
#                                                                    num_runs=exercise['runs'],
#                                                                    num_repeats=exercise['repeats'],
#                                                                    weight=exercise['weight'],
#                                                                    video_link=exercise['video_link']))
#     print(state_data['training'].training_exercises)
#
#     await message.answer(f'Прекрасно, так тренер сможет прокомментировать твою технику,  желаешь добавить еще одно упражнение?',
#                          reply_markup=create_add_exercise_keyboard())
#
#
# @add_training_router.callback_query(CreateTrainingCallback.filter(F.action == CreateTrainingCallbackActions.save))
#@callback_error_handler
# async def save_training(callback: CallbackQuery, callback_data: CreateTrainingCallback, state: FSMContext):
#     state_data = await state.get_data()
#     training = state_data['training']
#     print(training.training_exercises)
#     create_training(tg_id=callback.from_user.id, training=training)
#
#     await state.clear()
#     client = get_client_by_id(tg_id=callback.from_user.id)
#     if client.trainer:
#         await bot.send_message(chat_id=client.trainer.tg_id, text=f'{client.name} {client.surname}, https://t.me/{client.tg_username} только что добавил тренировку, заходи в его профиль и просмотри ее')
#     await callback.message.edit_text(f'Тренировка создана, мы вернулись в главное меню',
#                                      reply_markup=create_client_main_menu_keyboard())
#     await callback.answer()
# @add_training_router.callback_query(CreateTrainingCallback.filter(F.action == CreateTrainingCallbackActions.decline))
#@callback_error_handler
# async def decline_creation(callback: CallbackQuery, callback_data: CreateTrainingCallback, state: FSMContext):
#     await state.clear()
#     await callback.message.edit_text('Создание тренировки отклонено, мы снова в главном меню',
#                                      reply_markup=create_client_main_menu_keyboard())
#     await callback.answer()
#
# #Show trainings flow

