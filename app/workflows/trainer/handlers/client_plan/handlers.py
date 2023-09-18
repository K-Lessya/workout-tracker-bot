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
from app.entities.single_file.crud import get_trainer
from app.translations.base_translations import translations
client_plan_router = Router()


@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.show_client_plan_menu))
@callback_error_handler
async def show_plan_menu(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    client = state_data['client']
    await state.update_data({"lang": lang})
    kwargs = {
        'text': translations[lang].trainer_my_clients_menu_single_client_plan_menu.value,
        'reply_markup': ClientPlanMenuKeyboard(client, lang).as_markup()
    }
    if callback.message.photo:
        await callback.message.answer(**kwargs)
        await callback.message.delete()
    elif callback.message.text:
        await callback.message.edit_text(**kwargs)
    await callback.answer()


@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.show_client_plan_days))
@callback_error_handler
async def show_client_plan_days(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    lang = state_data['lang']
    await callback.message.edit_text(translations[lang].trainer_my_clients_menu_single_client_vieew_plan_show_days.value,
                                     reply_markup=ClientPlanDaysKeyboard(client.training_plan.days, lang).as_markup())
    await callback.answer()


@client_plan_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client_plan_day))
@callback_error_handler
async def show_client_plan_day(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    selected_day = int(callback_data.option)
    await state.update_data({'selected_day': selected_day})
    state_data = await state.get_data()
    lang = state_data['lang']
    client = state_data['client']
    exercises = client.training_plan.days[selected_day].training_exercises
    kwargs = {
        'text': translations[lang].trainer_my_clients_menu_single_client_vieew_plan_show_exercises.value,
        'reply_markup': ClientPlanExercisesKeyboard(plan_day_exercises=exercises, lang=lang).as_markup()
    }
    if callback.message.text:
        await callback.message.edit_text(**kwargs)
    elif callback.message.video or callback.message.photo:
        await callback.message.answer(**kwargs)
        await callback.message.delete()
    await callback.answer()


@client_plan_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client_plan_exercise))
@callback_error_handler
async def show_client_plan_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.delete()
    state_data = await state.get_data()
    lang = state_data['lang']
    notification = await bot.send_message(chat_id=callback.from_user.id,
                                          text=translations[lang]
                                          .trainer_my_clients_menu_single_client_view_plan_load_data.value)
    client = state_data['client']
    selected_day = state_data['selected_day']
    exercise = client.training_plan.days[selected_day].training_exercises[int(callback_data.option)]
    exercise_media_type = exercise.exercise.media_type
    exercise_media_link = create_presigned_url(PHOTO_BUCKET,exercise.exercise.media_link)
    print(exercise_media_link)
    kwargs = {
        'chat_id': callback.from_user.id,
        'caption': f"{exercise.exercise.name}\n{exercise.num_runs}x{exercise.num_repeats}\n"
                   f"{exercise.trainer_note}",
        'reply_markup': ClientPlanExerciseKeyboard(day=selected_day, lang=lang).as_markup()
    }

    if exercise_media_type == 'photo':
        await notification.edit_text(text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_photo
                                     .value)
        await state.update_data({'has_media': True})
        await bot.send_photo(photo=exercise_media_link, **kwargs)
        await notification.delete()
    elif exercise_media_type == 'video':
        await notification.edit_text(text=translations[lang].trainer_my_clients_menu_single_client_view_plan_get_video
                                     .value)
        file = URLInputFile(url=exercise_media_link, bot=bot)
        await notification.edit_text(text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_video
                                     .value)
        await bot.send_video(video=file, **kwargs)
        await notification.delete()
    await callback.answer()


