import requests, os
from aiogram import Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.workflows.client.utils.states import ClientStates
from app.bot import bot
from app.s3.downloader import create_presigned_url
from app.config import PHOTO_BUCKET
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.entities.training_plan.crud import get_training_days
from app.workflows.client.utils.keyboards.training_plan import TrainingDaysKeyboard, TrainingDayExercises,\
    PlanExerciseGoBackKeyboard
from app.workflows.client.utils.callback_properties.targets import ClientMyPlanTargets
from app.callbacks.callbacks import MoveCallback
from app.utilities.helpers_functions import callback_error_handler
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
my_plan_router = Router()


# Create training flow
@my_plan_router.callback_query(MoveCallback.filter(F.target == ClientMainMenuMoveTo.my_plan))
@callback_error_handler
async def start_creating_training(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    await callback.answer("Загружаю данные")
    await state.set_state(ClientStates.show_client_plan.show_days)
    training_days = get_training_days(client_id=callback.from_user.id)
    await state.update_data({'training_days': training_days})

    await callback.message.edit_text(f"Выбери день",
                                     reply_markup=TrainingDaysKeyboard(days=training_days,
                                                                       target=ClientMyPlanTargets.show_day,
                                                                       go_back_target=CommonGoBackMoveTo.to_client_main_menu).as_markup())

@my_plan_router.message(ClientStates.show_client_plan.show_days)
async def handle_message(message: Message, state: FSMContext):
    await message.delete()

@my_plan_router.callback_query(ChooseCallback.filter(F.target == ClientMyPlanTargets.show_day))
@callback_error_handler
async def show_day(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.answer("Загружаю данные")
    current_state = await state.get_state()

    await state.set_state(ClientStates.show_client_plan.show_exercises)
    state_data = await state.get_data()
    training_days = state_data['training_days']
    selected_day = training_days[int(callback_data.option)]
    await state.update_data({'selected_day': int(callback_data.option)})
    if callback.message.text:
        await callback.message.edit_text(f"Вот твои упражнения, для дня {int(callback_data.option)+1}, если не знаешь как"
                                     f" выполнять просто выбери упражнение из списка",
                                     reply_markup=TrainingDayExercises(selected_day.training_exercises,
                                                                       target=ClientMyPlanTargets.show_exercise,
                                                                       go_back_target=ClientMainMenuMoveTo.my_plan).as_markup())
    elif callback.message.photo or callback.message.video:
        await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id, text=f"Вот твои упражнения, для дня"
                                                                   f" {int(callback_data.option)+1}, если не знаешь как"
                                                                   f" выполнять просто выбери упражнение из списка",
                                     reply_markup=TrainingDayExercises(selected_day.training_exercises,
                                                                       target=ClientMyPlanTargets.show_exercise,
                                                                       go_back_target=ClientMainMenuMoveTo.my_plan).as_markup())

@my_plan_router.message(ClientStates.show_client_plan.show_exercises)
async def handle_message(message: Message, state: FSMContext):
    await message.delete()

@my_plan_router.callback_query(ChooseCallback.filter(F.target == ClientMyPlanTargets.show_exercise))
@callback_error_handler
async def show_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(ClientStates.show_client_plan.show_single_exercise)
    state_data = await state.get_data()
    training_days = state_data['training_days']
    selected_day = state_data['selected_day']
    selected_exercise = training_days[selected_day].training_exercises[int(callback_data.option)]
    media_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=selected_exercise.exercise.media_link)
    await callback.message.delete()
    await callback.answer('Загружаю файл, подождите', cache_time=10)

    exercise = selected_exercise
    exercise_media_type = exercise.exercise.media_type
    exercise_media_link = create_presigned_url(PHOTO_BUCKET, exercise.exercise.media_link)
    print(exercise_media_link)
    kwargs = {
        'chat_id': callback.from_user.id,
        'caption': f'{selected_exercise.exercise.name}\n{selected_exercise.num_runs} подхода'
                   f' по {selected_exercise.num_repeats} раз(а)',
        'reply_markup': PlanExerciseGoBackKeyboard(source_option=str(selected_day),
                                                   go_back_target=ClientMyPlanTargets.show_day).as_markup()
    }
    if exercise_media_type == 'photo':
        await state.update_data({'has_media': True})
        await bot.send_photo(photo=exercise_media_link, **kwargs)
    elif exercise_media_type == 'video':
        r = requests.get(exercise_media_link)

        filename = exercise_media_link.split('/')[-1].split('.')[0]
        open(f'tmp/{callback.from_user.id}-{filename}.mp4', 'wb').write(r.content)
        file = FSInputFile(f'tmp/{callback.from_user.id}-{filename}.mp4')
        await bot.send_video(video=file, **kwargs)

        os.remove(f'tmp/{callback.from_user.id}-{filename}.mp4')


@my_plan_router.message(ClientStates.show_client_plan.show_single_exercise)
async def handle_message(message: Message, state: FSMContext):
    await message.delete()
