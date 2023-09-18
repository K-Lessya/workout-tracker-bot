from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.bot import bot
from app.keyboards.yes_no import YesNoKeyboard
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback, YesNoOptions
from ..utils.keyboards.my_clients import MyClientsKeyboard, SingleClientKeyboard, ClientQuizKeyboard
from ..utils.callback_properties.movetos import TrainerMainMenuMoveTo, MyCLientsMoveTo
from ..utils.states import TrainerStates
from ..utils.callback_properties.targets import TrainerMyClientsTargets
from app.config import PHOTO_BUCKET
from app.entities.single_file.crud import *
from app.entities.exercise.crud import *
from app.s3.downloader import create_presigned_url
from ..utils.keyboards.exercise_db import ExercisePlanListKeyboard
from ..utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard
from ..utils.classes.training_plan import TrainingDay, TrainingPlan, PlanExercise
import logging
from app.entities.training_plan.training_plan import *
from app.workflows.trainer.handlers.client_trainings.handlers import my_clients_trainings_router
from app.entities.exercise.exercise import PlanTrainingExercise
from app.callbacks.callbacks import MoveCallback
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.types.menu_button_commands import MenuButtonCommands
from aiogram.types import WebAppInfo
from app.entities.single_file.crud import get_trainer
from app.utilities.helpers_functions import callback_error_handler
from app.workflows.trainer.utils.keyboards.next_action import NextActionKeyboard
from app.translations.base_translations import translations


my_clients_router = Router()
my_clients_router.include_router(my_clients_trainings_router)

@my_clients_router.callback_query(MoveToCallback.filter((F.move_to == TrainerMainMenuMoveTo.my_clients)|(F.move_to == MyCLientsMoveTo.show_next_clients)|(F.move_to == MyCLientsMoveTo.show_prev_clients)))
@callback_error_handler
async def show_my_clients_menu(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    await state.update_data({'lang': lang})
    clients = get_trainer_clients(trainer=trainer)
    if callback_data.move_to == TrainerMainMenuMoveTo.my_clients:
        await state.clear()
        await state.update_data({'start_index': 0})
        if clients:
            if callback.message.photo:
                await callback.message.delete()
                await bot.send_message(chat_id=callback.from_user.id,
                                       text=translations[lang].trainer_my_clients_menu_my_clients.value,
                                       reply_markup=MyClientsKeyboard(clients=clients, start_index=0, lang=lang).as_markup())
            else:
                await callback.message.edit_text(translations[lang].trainer_my_clients_menu_my_clients.value,
                                                 reply_markup=MyClientsKeyboard(clients=clients, start_index=0, lang=lang).as_markup())
            await callback.answer()
        else:
            clients = get_trainer_clients_witout_name(trainer=trainer)
            if clients:
                await callback.answer(translations[lang].trainer_my_clients_menu_no_clients_registered.value,
                                      show_alert=True)
            else:
                await callback.answer(translations[lang].trainer_my_clients_menu_no_clients.value, show_alert=True)
    elif callback_data.move_to == MyCLientsMoveTo.show_next_clients:
        state_data = await state.get_data()
        start_index = state_data['start_index']
        await state.update_data({'start_index': start_index+4})
        await callback.message.edit_reply_markup(reply_markup=MyClientsKeyboard(clients=clients, start_index=start_index+4, lang=lang).as_markup())
    elif callback_data.move_to == MyCLientsMoveTo.show_prev_clients:
        state_data = await state.get_data()
        start_index = state_data['start_index']
        await state.update_data({'start_index': start_index-4})
        await callback.message.edit_reply_markup(reply_markup=MyClientsKeyboard(clients=clients, start_index=start_index-4, lang=lang).as_markup())




@my_clients_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client))
@callback_error_handler
async def show_trainer_client(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    await state.update_data({'lang': lang})
    await bot.set_chat_menu_button(chat_id=callback.from_user.id, menu_button=MenuButtonCommands(type='commands'))
    client = get_client(obj_id=callback_data.option)
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=client.photo_link)
    await state.update_data({'client': client})

    await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                         caption=translations[lang].trainer_my_clients_menu_single_client_menu
                         .value.format(client.name,
                                       client.surname),
                         reply_markup=SingleClientKeyboard(client=client, lang=lang).as_markup())
    await callback.answer()

@my_clients_router.callback_query(MoveToCallback.filter(F.move_to == MyCLientsMoveTo.create_client_plan))
@callback_error_handler
async def create_plan_start(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    lang = state_data['lang']
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_days)
    await state.update_data({'plan': TrainingPlan()})

    if callback.message.photo:
        await callback.message.edit_caption(caption=translations[lang]
                                            .trainer_my_clients_menu_single_client_create_plan_start.value
                                            .format(client.name, client.surname))
    elif callback.message.text:
        await callback.message.edit_text(text=translations[lang]
                                         .trainer_my_clients_menu_single_client_create_plan_start.value
                                         .format(client.name, client.surname))
    await callback.answer()


@my_clients_router.message(TrainerStates.my_clients.create_plan.process_num_days)
async def process_num_days(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    if message.text.isdigit():
        plan = state_data['plan']
        plan.add_day(day=TrainingDay())
        await state.update_data({'plan': plan, 'num_days': int(message.text)})
        await state.set_state(TrainerStates.my_clients.create_plan.process_day_name)
        await message.answer(translations[lang].trainer_my_clients_menu_single_client_create_plan_day_name.value
                             .format(message.text, len(plan.days)))
    else:
        await message.answer(translations[lang].not_a_number_alert.value)



@my_clients_router.message(TrainerStates.my_clients.create_plan.process_day_name)
async def process_plan_day_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    lang = state_data['lang']
    current_day = plan.days[-1]
    current_day.add_name(message.text)
    await state.update_data({'plan': plan})
    body_parts = get_all_body_parts(trainer_id=get_trainer(message.from_user.id))
    if body_parts:
        await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
        await message.answer(translations[lang].trainer_my_clients_menu_single_client_create_plan_select_exercise.value
                             .format(len(plan.days)),
                             reply_markup=ExercisePlanListKeyboard(items=body_parts,
                                                                   tg_id=message.from_user.id,
                                                                   day_num=len(plan.days),
                                                                   lang=lang,
                                                                   exercises_length=len(current_day.exercises)).as_markup())
    else:
        await state.clear()
        await message.answer(translations[lang].trainer_my_clients_menu_single_client_create_plan_no_exercises.value,
                             reply_markup=create_trainer_main_menu_keyboard(lang=lang))


@my_clients_router.message(TrainerStates.my_clients.create_plan.process_body_parts)
async def process_message_on_body_parts(message: Message, state: FSMContext):
    await message.delete()


@my_clients_router.callback_query(MoveToCallback.filter(F.move_to == MyCLientsMoveTo.go_back_to_bodyparts_list))
async def show_body_parts(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    lang = state_data['lang']
    current_day = plan.days[-1]
    body_parts = get_all_body_parts(trainer_id=get_trainer(callback.from_user.id))
    if body_parts:
        await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
        await callback.message.edit_text(translations[lang]
                                         .trainer_my_clients_menu_single_client_create_plan_select_exercise.value
                                         .format(len(plan.days)),
                             reply_markup=ExercisePlanListKeyboard(items=body_parts,
                                                                   tg_id=callback.from_user.id,
                                                                   day_num=len(plan.days),
                                                                   lang=lang,
                                                                   exercises_length=len(
                                                                       current_day.exercises)).as_markup())



@my_clients_router.callback_query(ChooseCallback.filter((F.target == TrainerMyClientsTargets.choose_body_part) | (F.target == TrainerMyClientsTargets.choose_muscle_group) | (F.target == TrainerMyClientsTargets.choose_exercise_for_plan) | (F.target == TrainerMyClientsTargets.show_body_parts)))
@callback_error_handler
async def process_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    lang = state_data['lang']

    if callback_data.target == TrainerMyClientsTargets.choose_exercise_for_plan: #Чекаем что в кнопке находится упражнение
        exercise = get_exercise_by_id(callback_data.option)#Забираем упражнение из базы
        existing_exercises = [exercise.exercise.id for exercise in plan.days[-1].exercises]
        if exercise.id not in existing_exercises:
            plan.days[-1].add_exercise(PlanExercise(exercise))  #Добавляем упражнение в день плана
            keyboard = NextActionKeyboard(target=MyCLientsMoveTo.skip_trainer_note, lang=lang).as_markup()
            await state.update_data({'plan': plan}) #Обновляем состояние плана
            await state.set_state(TrainerStates.my_clients.create_plan.process_trainer_note) #Обновляем текущее состояние на процессинг количества подходов
            message_with_button = await callback.message.edit_text(text=translations[lang].
                                             trainer_my_clients_menu_single_client_create_plan_add_trainer_note.value,
                                             reply_markup=keyboard) #Отправляем сообщение
            await state.update_data({"to_delete_keyboard": message_with_button})
        else:
            await callback.answer(translations[lang].
                                  trainer_my_clietns_menu_single_client_create_plan_exercise_already_added.value,
                                  show_alert=True)
    else:
        if callback_data.target == TrainerMyClientsTargets.choose_body_part:
            body_part = get_body_part_by_id(callback_data.option)
            items = get_muscle_groups_by_body_part(body_part=body_part)
        elif callback_data.target == TrainerMyClientsTargets.choose_muscle_group:
            muscle_group = get_muscle_group_by_id(callback_data.option)
            items = get_exercises_by_muscle_group(muscle_group=muscle_group)
        elif callback_data.target == TrainerMyClientsTargets.show_body_parts:
            trainer = get_trainer(callback.from_user.id)
            items = get_all_body_parts(trainer)


        await callback.message.edit_reply_markup(
            reply_markup=ExercisePlanListKeyboard(items=items,
                                                  tg_id=callback.from_user.id,
                                                  exercises_length=len(plan.days[-1].exercises),
                                                  lang=lang,
                                                  day_num=len(plan.days)).as_markup())
    await callback.answer()


@my_clients_router.message(TrainerStates.my_clients.create_plan.process_trainer_note)
async def process_trainer_note(message: Message, state: FSMContext):
    state_data = await state.get_data()
    message_to_delete_keyboard = state_data["to_delete_keyboard"]
    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_to_delete_keyboard.message_id)
    plan = state_data['plan']
    lang = state_data['lang']
    plan.days[-1].exercises[-1].add_trainer_note(message.text)
    await state.update_data({'plan': plan})
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_runs)
    await message.answer(translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_runs.value)



@my_clients_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.skip_trainer_note))
async def skip_trainer_note(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    client = state_data['client']
    lang = state_data['lang']
    plan.days[-1].exercises[-1].add_trainer_note(
        translations[lang].trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added.value
    )
    await state.update_data({'plan': plan})
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_runs)
    await callback.message.edit_text(translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_runs.value)

@my_clients_router.message(TrainerStates.my_clients.create_plan.process_num_runs)
async def process_num_runs(message: Message, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    lang = state_data['lang']
    plan.days[-1].exercises[-1].add_runs(num_runs=int(message.text))
    await state.update_data({'plan': plan})
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_repeats)
    await message.answer(translations[lang].trainer_my_clietns_menu_single_client_create_plan_add_num_repeats.value)


@my_clients_router.message(TrainerStates.my_clients.create_plan.process_num_repeats)
async def process_num_repeats(message: Message, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    lang = state_data['lang']
    log_msg = '\nCurrent plan:\n'
    for idx, day in enumerate(plan.days):
        log_msg += f'  day {idx+1}:\n'
        for indx, exercise in enumerate(day.exercises):
            log_msg += f'    {indx+1}: {exercise.exercise.name}\n '
    logging.log(level=logging.DEBUG,
                msg=log_msg)
    plan.days[-1].exercises[-1].add_repeats(num_repeats=int(message.text))
    trainer = get_trainer(tg_id=message.from_user.id)
    body_parts = get_all_body_parts(trainer_id=trainer)
    await state.update_data({'plan': plan})
    await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
    await message.answer(translations[lang]. trainer_my_clietns_menu_single_client_create_plan_add_one_more_or_save_day.value,
                         reply_markup=ExercisePlanListKeyboard(items=body_parts,
                                                               tg_id=message.from_user.id,
                                                               day_num=len(plan.days),
                                                               lang=lang,
                                                               exercises_length=len(plan.days[-1].exercises)).as_markup())

@my_clients_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.save_plan))
@callback_error_handler
async def save_plan(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    lang = state_data['lang']
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=client.photo_link)

    if callback_data.option == YesNoOptions.yes:
        state_plan = state_data['plan']
        save_training_plan(state_plan, client)
        trainer = get_trainer(tg_id=callback.from_user.id)
        if len(str(client.tg_id)) == 9:
            await bot.send_message(chat_id=client.tg_id,
                                   text=translations[client.lang]
                                   .trainer_my_clients_menu_single_clietn_create_plan_save_client_notification.value
                                   .format(trainer.name, trainer.surname))
        await callback.answer(translations[lang].trainer_my_clients_menu_single_clietn_create_plan_save_trainer_alert.value,
                              show_alert=True)
        await callback.message.delete()
        await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                             caption=translations[lang].trainer_my_clients_menu_single_client_menu
                             .value.format(client.name, client.surname),
                             reply_markup=SingleClientKeyboard(client=client, lang=lang).as_markup())

    elif callback_data.option == YesNoOptions.no:
        state_data.pop('plan')
        state_data.pop('num_days')
        await state.update_data(state_data)
        await callback.answer('План не был сохранен', show_alert=True)
        await callback.message.delete()
        await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                             caption=translations[lang].trainer_my_clients_menu_single_client_menu
                             .value.format(client.name, client.surname),
                             reply_markup=SingleClientKeyboard(client=client, lang=lang).as_markup())

def save_training_plan(plan: TrainingPlan, client: Client):
    training_plan = DbTrainingPlan()
    for idx, day in enumerate(plan.days):
        training_plan.days.append(DbTrainingDay(name=day.day_name))
        for exercise in day.exercises:
            training_exercise = PlanTrainingExercise(exercise=exercise.exercise, num_runs=exercise.num_runs,
                                                     num_repeats=exercise.num_repeats, trainer_note=exercise.trainer_note)
            training_plan.days[idx].training_exercises.append(training_exercise)
    client.training_plan = training_plan
    client.save()



@my_clients_router.callback_query(MoveToCallback.filter(F.move_to == MyCLientsMoveTo.save_client_day))
@callback_error_handler
async def save_client_day(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    lang = state_data['lang']
    if len(plan.days) == state_data['num_days']:
        msg = ""
        for idx, day in enumerate(plan.days):
            msg += f"День {idx+1}\n"
            for ind, exercise in enumerate(day.exercises):
                msg += f"{ind+1}: {exercise.exercise.name}, {exercise.num_runs}X{exercise.num_repeats}\n"
        await callback.message.edit_text(text=translations[lang]
                                         .trainer_my_clients_menu_single_clietn_create_plan_save_plan_question.value,
                                         reply_markup=YesNoKeyboard(target=TrainerMyClientsTargets.save_plan, lang=lang)
                                         .as_markup())
    else:
        plan.add_day(TrainingDay())
        # body_parts = get_all_body_parts()
        # await callback.message.edit_text(text=f'Давай выберем упражнения для дня {len(plan.days)}',
        #                      reply_markup=ExercisePlanListKeyboard(items=body_parts,
        #                                                            day_num=len(plan.days),
        #                                                            exercises_length=len(plan.days[-1].exercises)).as_markup())
        await state.set_state(TrainerStates.my_clients.create_plan.process_day_name)
        await callback.message.edit_text(translations[lang].trainer_my_clients_menu_single_client_create_plan_day_name
                                         .value.format(state_data["num_days"], len(plan.days)))
    await callback.answer()




@my_clients_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.client_quiz))
@callback_error_handler
async def show_client_quiz(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    lang = state_data['lang']
    await bot.set_chat_menu_button(chat_id=callback.from_user.id,menu_button=MenuButtonWebApp(type='web_app', text="Показать анкету", web_app=WebAppInfo(url="https://aryzhykau.github.io/workout-bot-webapp/")))
    await callback.message.delete()
    await bot.send_message(chat_id=callback.from_user.id, text="Нажми на кнопку показать анкету", reply_markup=ClientQuizKeyboard(option=str(client.id)).as_markup())
    await callback.answer()

