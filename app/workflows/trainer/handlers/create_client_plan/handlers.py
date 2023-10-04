
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.utilities.helpers_functions import callback_error_handler
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.callbacks.callbacks import MoveCallback
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.translations.base_translations import translations
from app.workflows.trainer.utils.keyboards.next_action import NextActionKeyboard
from app.workflows.trainer.utils.states import TrainerStates
from app.workflows.trainer.utils.classes.training_plan import TrainingPlan, TrainingDay, PlanExercise
from app.workflows.trainer.utils.keyboards.create_plan_keyboards import CreatePlanStartKeyboard
from app.entities.training_plan.training_plan import DbTrainingPlan, DbTrainingDay, PlanTrainingExercise
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.entities.exercise.crud import get_all_body_parts, get_exercise_by_id, get_body_part_by_id, \
    get_muscle_groups_by_body_part, get_muscle_group_by_id, get_exercises_by_muscle_group
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.workflows.trainer.utils.keyboards.exercise_db import ExercisePlanListKeyboard
from app.bot import bot
from app.entities.training_plan.crud import create_new_plan, get_training_days, create_day, \
    get_last_plan_exercise, create_last_plan_exercise_num_runs, create_last_plan_exercise_num_repeats, \
    add_new_exercise_to_day, get_plans

create_plan_router = Router()


@create_plan_router.callback_query(MoveToCallback.filter(F.move_to == MyCLientsMoveTo.create_client_plan))
@callback_error_handler
async def create_plan_start(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    state_data = await state.get_data()
    client_id = state_data.get('client')
    client = get_client_by_id(client_id)
    lang = state_data.get('lang')
    if not get_plans(client):
        await callback.answer(translations[lang].trainer_create_plan_notification.value, show_alert=True)
    else:
        await callback.answer()
    await state.set_state(TrainerStates.my_clients.create_plan.process_start)
    create_new_plan(client)
    await state.update_data({'plan_id': -1})
    if callback.message.photo:
        await callback.message.edit_caption(caption=translations[lang]
                                            .trainer_my_clients_menu_single_client_create_plan_start.value
                                            .format(client.name, client.surname),
                                            reply_markup=CreatePlanStartKeyboard(client.id, lang).as_markup())
    elif callback.message.text:
        await callback.message.edit_text(text=translations[lang]
                                         .trainer_my_clients_menu_single_client_create_plan_start.value
                                         .format(client.name, client.surname),
                                         reply_markup=CreatePlanStartKeyboard(client.id, lang).as_markup())



@create_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.add_day_to_plan))
@callback_error_handler
async def add_new_day(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    client_id = state_data.get('client')
    plan_id = state_data.get('plan_id')
    days = get_training_days(client_id, plan_id=plan_id)
    await state.set_state(TrainerStates.my_clients.create_plan.process_day_name)
    if callback.message.photo:
        await callback.message.edit_caption(caption=translations[lang].trainer_my_clients_menu_single_client_create_plan_day_name.value.format(len(days)+1))
    elif callback.message.text:
        await callback.message.edit_text(text=translations[lang].trainer_my_clients_menu_single_client_create_plan_day_name.value.format(len(days)+1))


@create_plan_router.message(TrainerStates.my_clients.create_plan.process_day_name)
async def process_day_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    client_id = state_data.get('client')
    plan_id = state_data.get('plan_id')
    create_day(client_id, message.text, plan_id=plan_id)
    days = get_training_days(client_id, plan_id=plan_id)
    await state.update_data({'day_id': -1})
    await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
    trainer = get_trainer(message.from_user.id)
    body_parts = get_all_body_parts(trainer)
    print(len(days[-1].training_exercises))
    await message.answer("Давай добавим упражнения в план",
                         reply_markup=ExercisePlanListKeyboard(body_parts,
                                                               len(days[-1].training_exercises) if days[-1].training_exercises else 0,
                                                               message.from_user.id,
                                                               lang,
                                                               plan_id
                                                               ).as_markup())


@create_plan_router.callback_query(ChooseCallback.filter((F.target == TrainerMyClientsTargets.choose_body_part) | (F.target == TrainerMyClientsTargets.choose_muscle_group) | (F.target == TrainerMyClientsTargets.choose_exercise_for_plan) | (F.target == TrainerMyClientsTargets.show_body_parts)))
@callback_error_handler
async def process_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    day_id = state_data.get('day_id', -1)
    client_id = state_data.get('client')
    client = get_client_by_id(client_id)
    plan_id = state_data.get('plan_id')
    days = get_training_days(client_id, plan_id)
    day = days[day_id]
    print(day.name)
    lang = state_data['lang']
    print(callback_data.target)

    if callback_data.target == TrainerMyClientsTargets.choose_exercise_for_plan: #Чекаем что в кнопке находится упражнение
        exercise = get_exercise_by_id(callback_data.option)#Забираем упражнение из базы
        existing_exercises = [exercise.exercise.id for exercise in day.training_exercises]
        if exercise.id not in existing_exercises:
            add_new_exercise_to_day(client_id, plan_id, day_id, exercise)

            keyboard = NextActionKeyboard(target=MyCLientsMoveTo.skip_trainer_note, lang=lang).as_markup()
            await state.set_state(TrainerStates.my_clients.create_plan.process_trainer_note) #Обновляем текущее состояние на процессинг количества подходов
            message_with_button = await callback.message.edit_text(text=translations[lang].
                                             trainer_my_clients_menu_single_client_create_plan_add_trainer_note.value,
                                             reply_markup=keyboard) #Отправляем сообщение
            await state.update_data({"to_delete_keyboard": message_with_button})
        else:
            await callback.answer(translations[lang].
                                  trainer_my_clietns_menu_single_client_create_plan_exercise_already_added.value,
                                  show_alert=True)
  # Добавляем упражнение в день плана
    else:
        kwargs = {}
        if callback_data.target == TrainerMyClientsTargets.choose_body_part:
            body_part = get_body_part_by_id(callback_data.option)
            await state.update_data({'choosed_body_part_id': callback_data.option})
            items = get_muscle_groups_by_body_part(body_part=body_part)
        elif callback_data.target == TrainerMyClientsTargets.choose_muscle_group:
            muscle_group = get_muscle_group_by_id(callback_data.option)
            kwargs.update({'body_part_id': state_data.get('choosed_body_part_id', -1)})
            items = get_exercises_by_muscle_group(muscle_group=muscle_group)
        elif callback_data.target == TrainerMyClientsTargets.show_body_parts:
            trainer = get_trainer(callback.from_user.id)
            items = get_all_body_parts(trainer)


        await callback.message.edit_reply_markup(
            reply_markup=ExercisePlanListKeyboard(items=items,
                                                  tg_id=callback.from_user.id,
                                                  exercises_length=len(day.training_exercises),
                                                  lang=lang,
                                                  plan_id=plan_id,
                                                  **kwargs).as_markup())
    await callback.answer()


@create_plan_router.message(TrainerStates.my_clients.create_plan.process_trainer_note)
async def process_trainer_note(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    client_id = state_data.get('client')
    client = get_client_by_id(client_id)
    plan_id = state_data.get('plan_id')
    day_id = state_data.get('day_id', -1)
    days = get_training_days(client_id, plan_id)
    day = days[day_id]
    exercise = day.training_exercises[-1]
    message_to_delete_keyboard = state_data["to_delete_keyboard"]
    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_to_delete_keyboard.message_id)
    exercise.trainer_note = message.text
    client.save()
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_runs)
    await message.answer(translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_runs.value)



@create_plan_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.skip_trainer_note))
async def skip_trainer_note(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    client_id = state_data['client']
    lang = state_data.get('lang')
    client = get_client_by_id(client_id)
    plan_id = state_data.get('plan_id')
    day_id = state_data.get('day_id')
    days = get_training_days(client_id, plan_id)
    day = days[day_id]
    print(len(day.training_exercises))
    exercise = day.training_exercises[-1]
    exercise.trainer_note = translations[lang].trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added.value
    client.save()
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_runs)
    await callback.message.edit_text(translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_runs.value)


@create_plan_router.message(TrainerStates.my_clients.create_plan.process_num_runs)
async def process_num_runs(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    client_id = state_data.get('client')
    plan_id = state_data.get('plan_id')
    day_id = state_data.get('day_id', -1)
    if message.text.isdigit():
        create_last_plan_exercise_num_runs(client_id, int(message.text), plan_id, day_id)
        await state.set_state(TrainerStates.my_clients.create_plan.process_num_repeats)
        msg = translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_repeats.value
    else:
        msg = translations[lang].client_number_required.value
    await message.answer(msg)


@create_plan_router.message(TrainerStates.my_clients.create_plan.process_num_repeats)
async def process_num_repeats(message: Message, state: FSMContext):
    state_data = await state.get_data()
    client_id = state_data.get('client')
    lang = state_data.get('lang')
    plan_id = state_data.get('plan_id')
    day_id = state_data.get('day_id', -1)
    create_last_plan_exercise_num_repeats(client_id, int(message.text), plan_id, day_id)
    days = get_training_days(client_id, plan_id)
    trainer = get_trainer(tg_id=message.from_user.id)
    body_parts = get_all_body_parts(trainer_id=trainer)
    await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
    await message.answer(translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_one_more_or_save_day.value,
                         reply_markup=ExercisePlanListKeyboard(items=body_parts,
                                                               tg_id=message.from_user.id,
                                                               lang=lang,
                                                               plan_id=plan_id,
                                                               exercises_length=len(days[day_id].training_exercises)).as_markup())

# @my_clients_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.save_plan))
# @callback_error_handler
# async def save_plan(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
#     state_data = await state.get_data()
#     client = state_data['client']
#     lang = state_data['lang']
#     photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=client.photo_link)
#
#     if callback_data.option == YesNoOptions.yes:
#         state_plan = state_data['plan']
#         save_training_plan(state_plan, client)
#         trainer = get_trainer(tg_id=callback.from_user.id)
#         if len(str(client.tg_id)) == 9:
#             await bot.send_message(chat_id=client.tg_id,
#                                    text=translations[client.lang]
#                                    .trainer_my_clients_menu_single_clietn_create_plan_save_client_notification.value
#                                    .format(trainer.name, trainer.surname))
#         await callback.answer(translations[lang].trainer_my_clients_menu_single_clietn_create_plan_save_trainer_alert.value,
#                               show_alert=True)
#         await callback.message.delete()
#         await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
#                              caption=translations[lang].trainer_my_clients_menu_single_client_menu
#                              .value.format(client.name, client.surname),
#                              reply_markup=SingleClientKeyboard(client=client, lang=lang).as_markup())
#
#     elif callback_data.option == YesNoOptions.no:
#         state_data.pop('plan')
#         state_data.pop('num_days')
#         await state.update_data(state_data)
#         await callback.answer('План не был сохранен', show_alert=True)
#         await callback.message.delete()
#         await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
#                              caption=translations[lang].trainer_my_clients_menu_single_client_menu
#                              .value.format(client.name, client.surname),
#                              reply_markup=SingleClientKeyboard(client=client, lang=lang).as_markup())
#
#
# def save_training_plan(plan: TrainingPlan, client: Client):
#     training_plan = DbTrainingPlan()
#     for idx, day in enumerate(plan.days):
#         training_plan.days.append(DbTrainingDay(name=day.day_name))
#         for exercise in day.exercises:
#             training_exercise = PlanTrainingExercise(exercise=exercise.exercise, num_runs=exercise.num_runs,
#                                                      num_repeats=exercise.num_repeats, trainer_note=exercise.trainer_note)
#             training_plan.days[idx].training_exercises.append(training_exercise)
#     client.training_plan = training_plan
#     client.save()
#
#
#
# @my_clients_router.callback_query(MoveToCallback.filter(F.move_to == MyCLientsMoveTo.save_client_day))
# @callback_error_handler
# async def save_client_day(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
#     state_data = await state.get_data()
#     plan = state_data['plan']
#     lang = state_data['lang']
#     if len(plan.days) == state_data['num_days']:
#         msg = ""
#         for idx, day in enumerate(plan.days):
#             msg += f"День {idx+1}\n"
#             for ind, exercise in enumerate(day.exercises):
#                 msg += f"{ind+1}: {exercise.exercise.name}, {exercise.num_runs}X{exercise.num_repeats}\n"
#         await callback.message.edit_text(text=translations[lang]
#                                          .trainer_my_clients_menu_single_clietn_create_plan_save_plan_question.value,
#                                          reply_markup=YesNoKeyboard(target=TrainerMyClientsTargets.save_plan, lang=lang)
#                                          .as_markup())
#     else:
#         plan.add_day(TrainingDay())
#         # body_parts = get_all_body_parts()
#         # await callback.message.edit_text(text=f'Давай выберем упражнения для дня {len(plan.days)}',
#         #                      reply_markup=ExercisePlanListKeyboard(items=body_parts,
#         #                                                            day_num=len(plan.days),
#         #                                                            exercises_length=len(plan.days[-1].exercises)).as_markup())
#         await state.set_state(TrainerStates.my_clients.create_plan.process_day_name)
#         await callback.message.edit_text(translations[lang].trainer_my_clients_menu_single_client_create_plan_day_name
#                                          .value.format(state_data["num_days"], len(plan.days)))
#     await callback.answer()
#
#
#
