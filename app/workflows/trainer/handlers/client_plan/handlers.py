import requests
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, URLInputFile, Message
from aiogram.fsm.context import FSMContext
from app.bot import bot
from app.callbacks.callbacks import MoveCallback, ChooseCallback
from app.entities.exercise.crud import get_all_body_parts
from app.entities.training_plan.crud import get_single_plan, get_training_days, edit_exercise_num_runs, \
    get_plan_exercise, get_day_exercises, edit_exercise_num_repeats, edit_exercise_trainer_note, publish_new_plan
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.workflows.trainer.utils.keyboards.clients_plan import ClientPlanMenuKeyboard, ClientPlanDaysKeyboard, \
    ClientPlanExercisesKeyboard, ClientPlanExerciseKeyboard
from app.s3.downloader import create_presigned_url
from app.config import PHOTO_BUCKET
from app.utilities.helpers_functions import callback_error_handler, double_button_click_handler
from app.entities.single_file.crud import get_trainer
from app.translations.base_translations import translations
from app.entities.single_file.crud import get_client_by_id
from app.workflows.trainer.utils.keyboards.exercise_db import ExercisePlanListKeyboard
from app.workflows.trainer.utils.states import TrainerStates

client_plan_router = Router()


@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.show_client_plan_menu))
@callback_error_handler
async def show_plan_menu(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    client_id = state_data['client']
    client = get_client_by_id(client_id)


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


@client_plan_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client_plans))
@callback_error_handler
async def show_client_plan_days(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    client_id = state_data['client']
    client = get_client_by_id(client_id)
    lang = state_data['lang']
    await state.update_data({'plan_id': int(callback_data.option)})
    plan = get_single_plan(client_id, int(callback_data.option))

    await callback.message.edit_text(translations[lang].trainer_my_clients_menu_single_client_vieew_plan_show_days.value,
                                     reply_markup=ClientPlanDaysKeyboard(plan.days, lang).as_markup())
    await callback.answer()


@client_plan_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client_plan_day))
@callback_error_handler
async def show_client_plan_day(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    selected_day = int(callback_data.option)
    await state.update_data({'selected_day': selected_day, 'day_id': selected_day})
    state_data = await state.get_data()
    plan_id = state_data.get('plan_id', -1)
    lang = state_data['lang']
    client_id = state_data['client']
    client = get_client_by_id(client_id)
    exercises = client.training_plans[plan_id].days[selected_day].training_exercises
    kwargs = {
        'text': translations[lang].trainer_my_clients_menu_single_client_vieew_plan_show_exercises.value,
        'reply_markup': ClientPlanExercisesKeyboard(plan_day_exercises=exercises, lang=lang, plan_id=plan_id).as_markup()
    }
    if callback.message.text:
        await callback.message.edit_text(**kwargs)
    elif callback.message.video or callback.message.photo:
        await callback.message.answer(**kwargs)
        await callback.message.delete()
    await callback.answer()


@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.add_exercise_to_day))
@callback_error_handler
async def add_exercise_to_day(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    plan_id = state_data.get('plan_id', -1)
    day_id = state_data.get('day_id', -1)
    client_id = state_data.get('client')
    trainer = get_trainer(callback.from_user.id)
    days = get_training_days(client_id, plan_id)
    await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
    body_parts = get_all_body_parts(trainer)
    await callback.message.edit_text(text=translations[lang].trainer_create_plan_choose_exercise_for_day.value,
                                     reply_markup=ExercisePlanListKeyboard(body_parts,
                                                               len(days[day_id].training_exercises),
                                                               callback.from_user.id,
                                                               lang,
                                                               plan_id,

                                                               ).as_markup())

@client_plan_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client_plan_exercise))
@callback_error_handler
async def show_client_plan_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.delete()
    await state.update_data({'exercise_id': callback_data.option})
    state_data = await state.get_data()
    lang = state_data['lang']
    notification = await bot.send_message(chat_id=callback.from_user.id,
                                          text=translations[lang]
                                          .trainer_my_clients_menu_single_client_view_plan_load_data.value)
    client_id = state_data['client']
    plan_id = state_data.get('plan_id', -1)
    client = get_client_by_id(client_id)
    selected_day = state_data['selected_day']

    exercise = client.training_plans[plan_id].days[selected_day].training_exercises[int(callback_data.option)]
    exercise_media_type = exercise.exercise.media_type
    exercise_media_link = create_presigned_url(PHOTO_BUCKET,exercise.exercise.media_link)
    print(exercise_media_link)
    kwargs = {
        'chat_id': callback.from_user.id,
        'caption': (f"{exercise.exercise.name}\n{exercise.num_runs}x{exercise.num_repeats}\n")
                   + (f"{exercise.trainer_note}" if exercise.trainer_note
        else translations[lang].trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added.value),
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




@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.change_num_runs))
@callback_error_handler
async def change_num_runs_callback(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    await state.set_state(TrainerStates.my_clients.edit_plan_exercise.edit_num_runs)
    await callback.message.edit_caption(caption=translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_runs.value)


@client_plan_router.message(TrainerStates.my_clients.edit_plan_exercise.edit_num_runs)
async def process_edit_num_runs(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    if message.text.isdigit():
        client_id = state_data.get('client')
        exercise_id = int(state_data.get('exercise_id', -1))
        plan_id = state_data.get('plan_id', -1)
        day_id = state_data.get('day_id', -1)
        exercise = get_plan_exercise(client_id, plan_id, day_id, exercise_id)
        edit_exercise_num_runs(client_id, plan_id, day_id, exercise_id, int(message.text))
        selected_day = state_data.get('selected_day')
        exercise_media_type = exercise.exercise.media_type
        exercise_media_link = create_presigned_url(PHOTO_BUCKET, exercise.exercise.media_link)
        notification = await bot.send_message(chat_id=message.from_user.id,
                                              text=translations[lang]
                                              .trainer_my_clients_menu_single_client_view_plan_load_data.value)
        kwargs = {
            'chat_id': message.from_user.id,
            'caption': (f"{exercise.exercise.name}\n{message.text}x{exercise.num_repeats}\n")
                       + (f"{exercise.trainer_note}" if exercise.trainer_note
                          else translations[lang]
                          .trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added.value),
            'reply_markup': ClientPlanExerciseKeyboard(day=selected_day, lang=lang).as_markup()
        }

        if exercise_media_type == 'photo':
            await notification.edit_text(
                text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_photo
                .value)
            await state.update_data({'has_media': True})
            await bot.send_photo(photo=exercise_media_link, **kwargs)
            await notification.delete()
        elif exercise_media_type == 'video':
            await notification.edit_text(
                text=translations[lang].trainer_my_clients_menu_single_client_view_plan_get_video
                .value)
            file = URLInputFile(url=exercise_media_link, bot=bot)
            await notification.edit_text(
                text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_video
                .value)
            await bot.send_video(video=file, **kwargs)
            await notification.delete()
    else:
        await message.answer(translations[lang].client_number_required.value)



@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.change_num_repeats))
@callback_error_handler
async def change_num_repeats_callback(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    await state.set_state(TrainerStates.my_clients.edit_plan_exercise.edit_num_repeats)
    await callback.message.edit_caption(caption=translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_repeats.value)


@client_plan_router.message(TrainerStates.my_clients.edit_plan_exercise.edit_num_repeats)
async def process_edit_num_runs(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    if message.text.isdigit():
        client_id = state_data.get('client')
        exercise_id = int(state_data.get('exercise_id', -1))
        plan_id = state_data.get('plan_id', -1)
        day_id = state_data.get('day_id', -1)
        exercise = get_plan_exercise(client_id, plan_id, day_id, exercise_id)
        edit_exercise_num_repeats(client_id, plan_id, day_id, exercise_id, int(message.text))
        selected_day = state_data.get('selected_day')
        exercise_media_type = exercise.exercise.media_type
        exercise_media_link = create_presigned_url(PHOTO_BUCKET, exercise.exercise.media_link)
        notification = await bot.send_message(chat_id=message.from_user.id,
                                              text=translations[lang]
                                              .trainer_my_clients_menu_single_client_view_plan_load_data.value)
        kwargs = {
            'chat_id': message.from_user.id,
            'caption': (f"{exercise.exercise.name}\n{exercise.num_runs}x{message.text}\n")
                       + (f"{exercise.trainer_note}" if exercise.trainer_note
                          else translations[lang]
                          .trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added.value),
            'reply_markup': ClientPlanExerciseKeyboard(day=selected_day, lang=lang).as_markup()
        }

        if exercise_media_type == 'photo':
            await notification.edit_text(
                text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_photo
                .value)
            await state.update_data({'has_media': True})
            await bot.send_photo(photo=exercise_media_link, **kwargs)
            await notification.delete()
        elif exercise_media_type == 'video':
            await notification.edit_text(
                text=translations[lang].trainer_my_clients_menu_single_client_view_plan_get_video
                .value)
            file = URLInputFile(url=exercise_media_link, bot=bot)
            await notification.edit_text(
                text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_video
                .value)
            await bot.send_video(video=file, **kwargs)
            await notification.delete()
    else:
        await message.answer(translations[lang].client_number_required.value)




@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.change_trainer_note))
@callback_error_handler
async def change_trainer_note_callback(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    await state.set_state(TrainerStates.my_clients.edit_plan_exercise.edit_trainer_note)
    await callback.message.edit_caption(caption=translations[lang].trainer_my_clients_menu_single_client_create_plan_add_trainer_note.value)


@client_plan_router.message(TrainerStates.my_clients.edit_plan_exercise.edit_trainer_note)
async def process_edit_trainer_note(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    client_id = state_data.get('client')
    exercise_id = int(state_data.get('exercise_id', -1))
    plan_id = state_data.get('plan_id', -1)
    day_id = state_data.get('day_id', -1)
    exercise = get_plan_exercise(client_id, plan_id, day_id, exercise_id)
    edit_exercise_trainer_note(client_id, plan_id, day_id, exercise_id, message.text)
    exercise = get_plan_exercise(client_id, plan_id, day_id, exercise_id)
    selected_day = state_data.get('selected_day')
    exercise_media_type = exercise.exercise.media_type
    exercise_media_link = create_presigned_url(PHOTO_BUCKET, exercise.exercise.media_link)
    notification = await bot.send_message(chat_id=message.from_user.id,
                                          text=translations[lang]
                                          .trainer_my_clients_menu_single_client_view_plan_load_data.value)
    kwargs = {
        'chat_id': message.from_user.id,
        'caption': (f"{exercise.exercise.name}\n{exercise.num_runs}x{exercise.num_repeats}\n")
                   + (f"{message.text}" if exercise.trainer_note
                      else translations[lang]
                      .trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added.value),
        'reply_markup': ClientPlanExerciseKeyboard(day=selected_day, lang=lang).as_markup()
    }

    if exercise_media_type == 'photo':
        await notification.edit_text(
            text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_photo
            .value)
        await state.update_data({'has_media': True})
        await bot.send_photo(photo=exercise_media_link, **kwargs)
        await notification.delete()
    elif exercise_media_type == 'video':
        await notification.edit_text(
            text=translations[lang].trainer_my_clients_menu_single_client_view_plan_get_video
            .value)
        file = URLInputFile(url=exercise_media_link, bot=bot)
        await notification.edit_text(
            text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_video
            .value)
        await bot.send_video(video=file, **kwargs)
        await notification.delete()


@client_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.publish_plan))
@callback_error_handler
async def publish_plan(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    client_id = state_data.get('client')
    plan_id = state_data.get('plan_id')
    publish_new_plan(client_id, plan_id)
    await callback.answer(translations[lang].trainer_my_clients_menu_single_client_publish_plan_notification.value, show_alert=True)