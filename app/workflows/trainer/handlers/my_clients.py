from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.bot import bot
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
from app.utilities.default_keyboards.yes_no import YesNoKeyboard
from app.entities.training_plan.training_plan import *
from app.workflows.trainer.handlers.client_trainings.handlers import my_clients_trainings_router
from app.entities.exercise.exercise import PlanTrainingExercise
from app.callbacks.callbacks import MoveCallback
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.types.menu_button_commands import MenuButtonCommands
from aiogram.types import WebAppInfo
from app.utilities.helpers_functions import callback_error_handler
my_clients_router = Router()
my_clients_router.include_router(my_clients_trainings_router)

@my_clients_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_client))
@callback_error_handler
async def show_trainer_client(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await bot.set_chat_menu_button(chat_id=callback.from_user.id, menu_button=MenuButtonCommands(type='commands'))
    client = get_client(obj_id=callback_data.option)
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=client.photo_link)
    await state.update_data({'client': client})

    await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                         caption=f"Клиент:\nИмя: {client.name}\nФамилия: {client.surname}",
                         reply_markup=SingleClientKeyboard(client=client).as_markup())
    await callback.answer("Загрузка завершена")


@my_clients_router.callback_query(MoveToCallback.filter(F.move_to == MyCLientsMoveTo.create_client_plan))
@callback_error_handler
async def create_plan_start(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_days)
    await state.update_data({'plan': TrainingPlan()})
    if callback.message.photo:
        await callback.message.edit_caption(caption=f"Составляем план для клиента {client.name} {client.surname}.\n"
                                     f"Введи количество дней в плане")
    elif callback.message.text:
        await callback.message.edit_text(text=f"Составляем план для клиента {client.name} {client.surname}.\n"
                                     f"Введи количество дней в плане")
    await callback.answer("Загрузка завершена")

@my_clients_router.message(TrainerStates.my_clients.create_plan.process_num_days)
async def process_num_days(message: Message, state: FSMContext):
    if message.text.isdigit():
        state_data = await state.get_data()
        plan = state_data['plan']
        plan.add_day(day=TrainingDay())
        await state.update_data({'plan': plan, 'num_days': int(message.text)})
        await state.set_state(TrainerStates.my_clients.create_plan.process_day_name)
        await message.answer(f'В плане {message.text} дней, введи название дня {len(plan.days)}')
    else:
        await message.answer('Я ожидаю число')


@my_clients_router.message(TrainerStates.my_clients.create_plan.process_day_name)
async def process_plan_day_name(message: Message, state: FSMContext):
        state_data = await state.get_data()
        plan = state_data['plan']
        current_day = plan.days[-1]
        current_day.add_name(message.text)
        await state.update_data({'plan': plan})
        body_parts = get_all_body_parts()
        if body_parts:
            await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
            await message.answer(f'Давай выберем упражнения для дня {len(plan.days)}',
                                 reply_markup=ExercisePlanListKeyboard(items=body_parts,
                                                                       day_num=len(plan.days),
                                                                       exercises_length=len(current_day.exercises)).as_markup())
        else:
            await state.clear()
            await message.answer(f'В базе еще нет ни одного упражнения, добавь их через меню', reply_markup=create_trainer_main_menu_keyboard())

@my_clients_router.callback_query(MoveToCallback.filter(F.move_to == TrainerMainMenuMoveTo.my_clients))
@callback_error_handler
async def show_my_clients_menu(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    await state.clear()
    trainer = get_trainer(callback.from_user.id)
    clients = get_trainer_clients(trainer=trainer)
    if clients:
        if callback.message.photo:
            await callback.message.delete()
            await bot.send_message(chat_id=callback.from_user.id, text="Мои клиенты. Выбирай нужного",
                                   reply_markup=MyClientsKeyboard(clients=clients).as_markup())
        else:
            await callback.message.edit_text("Мои клиенты. Выбирай нужного",
                                             reply_markup=MyClientsKeyboard(clients=clients).as_markup())
        await callback.answer("Загрузка завершена")
    else:
        clients = get_trainer_clients_witout_name(trainer=trainer)
        if clients:
            await callback.answer("Ни один из клиентов пока не зарегистрировался или не принял заявку", show_alert=True)
        else:
            await callback.answer("Клиентов пока нет", show_alert=True)



@my_clients_router.message(TrainerStates.my_clients.create_plan.process_num_runs)
async def process_num_runs(message: Message, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    plan.days[-1].exercises[-1].add_runs(num_runs=int(message.text))
    await state.update_data({'plan': plan})
    await state.set_state(TrainerStates.my_clients.create_plan.process_num_repeats)
    await message.answer('А теперь количество повторений за подход')


@my_clients_router.callback_query(ChooseCallback.filter((F.target == TrainerMyClientsTargets.choose_body_part) | (F.target == TrainerMyClientsTargets.choose_muscle_group) | (F.target == TrainerMyClientsTargets.choose_exercise_for_plan)))
@callback_error_handler
async def process_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']

    if callback_data.target == TrainerMyClientsTargets.choose_exercise_for_plan: #Чекаем что в кнопке находится упражнение
        exercise = get_exercise_by_id(callback_data.option) #Забираем упражнение из базы
        plan.days[-1].add_exercise(PlanExercise(exercise))  #Добавляем упражнение в день плана

        await state.update_data({'plan': plan}) #Обновляем состояние плана
        await state.set_state(TrainerStates.my_clients.create_plan.process_num_runs) #Обновляем текущее состояние на процессинг количества подходов
        await callback.message.edit_text(text="А теперь введи количество подходов") #Отправляем сообщение
    else:
        if callback_data.target == TrainerMyClientsTargets.choose_body_part:
            body_part = get_body_part_by_id(callback_data.option)
            items = get_muscle_groups_by_body_part(body_part=body_part)
        elif callback_data.target == TrainerMyClientsTargets.choose_muscle_group:
            muscle_group = get_muscle_group_by_id(callback_data.option)
            items = get_exercises_by_muscle_group(muscle_group=muscle_group)

        await callback.message.edit_reply_markup(
            reply_markup=ExercisePlanListKeyboard(items=items,
                                                  exercises_length=len(plan.days[-1].exercises),
                                                  day_num=len(plan.days)).as_markup())
    await callback.answer("Загрузка завершена")


@my_clients_router.message(TrainerStates.my_clients.create_plan.process_num_repeats)
async def process_num_repeats(message: Message, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    log_msg = '\nCurrent plan:\n'
    for idx, day in enumerate(plan.days):
        log_msg += f'  day {idx+1}:\n'
        for indx, exercise in enumerate(day.exercises):
            log_msg += f'    {indx+1}: {exercise.exercise.name}\n '
    logging.log(level=logging.DEBUG,
                msg=log_msg)
    plan.days[-1].exercises[-1].add_repeats(num_repeats=int(message.text))
    body_parts = get_all_body_parts()
    await state.update_data({'plan': plan})
    await state.set_state(TrainerStates.my_clients.create_plan.process_body_parts)
    await message.answer('Отлично, теперь давай добавим следующее упражнение либо сохраним день',
                         reply_markup=ExercisePlanListKeyboard(items=body_parts,
                                                               day_num=len(plan.days),
                                                               exercises_length=len(plan.days[-1].exercises)).as_markup())

@my_clients_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.save_plan))
@callback_error_handler
async def save_plan(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=client.photo_link)

    if callback_data.option == YesNoOptions.yes:
        state_plan = state_data['plan']
        save_training_plan(state_plan, client)
        await callback.answer('План сохранен, клиент может его просмотреть', show_alert=True)
        await callback.message.delete()
        await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                             caption=f"Клиент:\nИмя: {client.name}\nФамилия: {client.surname}",
                             reply_markup=SingleClientKeyboard(client=client).as_markup())

    elif callback_data.option == YesNoOptions.no:
        state_data.pop('plan')
        state_data.pop('num_days')
        await state.update_data(state_data)
        await callback.answer('План не был сохранен', show_alert=True)
        await callback.message.delete()
        await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                             caption=f"Клиент:\nИмя: {client.name}\nФамилия: {client.surname}",
                             reply_markup=SingleClientKeyboard(client=client).as_markup())

def save_training_plan(plan: TrainingPlan, client: Client):
    training_plan = DbTrainingPlan()
    for idx, day in enumerate(plan.days):
        training_plan.days.append(DbTrainingDay(name=day.day_name))
        for exercise in day.exercises:
            training_exercise = PlanTrainingExercise(exercise=exercise.exercise, num_runs=exercise.num_runs,
                                                     num_repeats=exercise.num_repeats)
            training_plan.days[idx].training_exercises.append(training_exercise)
    client.training_plan = training_plan
    client.save()



@my_clients_router.callback_query(MoveToCallback.filter(F.move_to == MyCLientsMoveTo.save_client_day))
@callback_error_handler
async def save_client_day(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    state_data = await state.get_data()
    plan = state_data['plan']
    if len(plan.days) == state_data['num_days']:
        msg = ""
        for idx, day in enumerate(plan.days):
            msg += f"День {idx+1}\n"
            for ind, exercise in enumerate(day.exercises):
                msg += f"{ind+1}: {exercise.exercise.name}, {exercise.num_runs}X{exercise.num_repeats}\n"
        await callback.message.edit_text(text='Сохраняем план?',
                                         reply_markup=YesNoKeyboard(target=TrainerMyClientsTargets.save_plan).as_markup())
    else:
        plan.add_day(TrainingDay())
        # body_parts = get_all_body_parts()
        # await callback.message.edit_text(text=f'Давай выберем упражнения для дня {len(plan.days)}',
        #                      reply_markup=ExercisePlanListKeyboard(items=body_parts,
        #                                                            day_num=len(plan.days),
        #                                                            exercises_length=len(plan.days[-1].exercises)).as_markup())
        await state.set_state(TrainerStates.my_clients.create_plan.process_day_name)
        await callback.message.edit_text(f'В плане {state_data["num_days"]} дней. Введи название дня {len(plan.days)} ')
    await callback.answer("Загрузка завершена")




@my_clients_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.client_quiz))
@callback_error_handler
async def show_client_quiz(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    client = state_data['client']
    await bot.set_chat_menu_button(chat_id=callback.from_user.id,menu_button=MenuButtonWebApp(type='web_app', text="Показать анкету", web_app=WebAppInfo(url="https://aryzhykau.github.io/workout-bot-webapp/")))
    await callback.message.delete()
    await bot.send_message(chat_id=callback.from_user.id, text="Нажми на кнопку показать анкету", reply_markup=ClientQuizKeyboard(option=str(client.id)).as_markup())
    await callback.answer("Загрузка завершена")

