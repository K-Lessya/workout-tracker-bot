import requests
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, URLInputFile
from aiogram.fsm.context import FSMContext
from app.bot import bot
from app.callbacks.callbacks import MoveCallback, ChooseCallback
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.workflows.trainer.utils.keyboards.clients_plan import ClientPlanMenuKeyboard, ClientPlanDaysKeyboard, \
    ClientPlanExercisesKeyboard, ClientPlanExerciseKeyboard
from app.s3.downloader import create_presigned_url
from app.config import PHOTO_BUCKET
from app.utilities.helpers_functions import callback_error_handler, double_button_click_handler
client_plan_router = Router()

@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.show_client_plan_menu))
@callback_error_handler
async def show_plan_menu(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    kwargs = {
        'text': "Выбери просмотреть план или cоздать новый план",
        'reply_markup': ClientPlanMenuKeyboard(client).as_markup()
    }
    if callback.message.photo:
        await callback.message.answer(**kwargs)
        await callback.message.delete()
    elif callback.message.text:
        await callback.message.edit_text(**kwargs)
    await callback.answer("Загрузка завершена")
@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.show_client_plan_days))
@callback_error_handler
async def show_client_plan_days(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    await callback.message.edit_text("Выбери день из плана",
                                     reply_markup=ClientPlanDaysKeyboard(client.training_plan.days).as_markup())
    await callback.answer("Загрузка завершена")


@client_plan_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client_plan_day))
@callback_error_handler
async def show_client_plan_day(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    selected_day = int(callback_data.option)
    await state.update_data({'selected_day': selected_day})
    state_data = await state.get_data()
    client = state_data['client']
    exercises = client.training_plan.days[selected_day].training_exercises
    kwargs = {
        'text': "Выбери упражнение",
        'reply_markup': ClientPlanExercisesKeyboard(plan_day_exercises=exercises).as_markup()
    }
    if callback.message.text:
        await callback.message.edit_text(**kwargs)
    elif callback.message.video or callback.message.photo:
        await callback.message.answer(**kwargs)
        await callback.message.delete()
    await callback.answer("Загрузка завершена")

@client_plan_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client_plan_exercise))
@callback_error_handler
async def show_client_plan_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.delete()
    notification = await bot.send_message(chat_id=callback.from_user.id, text="Заргружаю данные")
    state_data = await state.get_data()
    client = state_data['client']
    selected_day = state_data['selected_day']
    exercise = client.training_plan.days[selected_day].training_exercises[int(callback_data.option)]
    exercise_media_type = exercise.exercise.media_type
    exercise_media_link = create_presigned_url(PHOTO_BUCKET,exercise.exercise.media_link)
    print(exercise_media_link)
    kwargs = {
        'chat_id': callback.from_user.id,
        'caption': f"{exercise.exercise.name}\n{exercise.num_runs}x{exercise.num_repeats}",
        'reply_markup': ClientPlanExerciseKeyboard(day=selected_day).as_markup()
    }

    if exercise_media_type == 'photo':
        await notification.edit_text(text="Отправляю фото")
        await state.update_data({'has_media': True})
        await bot.send_photo(photo=exercise_media_link, **kwargs)
        await notification.delete()
    elif exercise_media_type == 'video':
        await notification.edit_text(text='Получаю видео')
        file = URLInputFile(url=exercise_media_link, bot=bot)
        await notification.edit_text(text="Отправляю видео")
        await bot.send_video(video=file, **kwargs)
        await notification.delete()
    await callback.answer("Загрузка завершена")


