import locale
import requests
from aiogram import Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.config import PHOTO_BUCKET, LOCALE
from app.bot import bot
from app.s3.downloader import create_presigned_url
from app.entities.single_file.crud import get_client_trainings, get_client_training
from app.callbacks.callbacks import MoveCallback
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.client.utils.callback_properties.movetos import MyTrainingsMoveTo, ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientMyTrainingsTarget
from app.workflows.client.classes.my_trainings import MyTrainings, MyTrainingsOption
from app.keyboards.trainings.keyboard import PaginationKeyboard, TrainingExercisesKeyboard,\
    TrainingSingleExerciseKeyboard, TrainingVideoKeyboard


my_trainings_router = Router()




@my_trainings_router.callback_query(MoveCallback.filter((F.target == ClientMainMenuMoveTo.my_trainings) |
                                                        (F.target == MyTrainingsMoveTo.to_prev_trainings) |
                                                        (F.target == MyTrainingsMoveTo.to_next_trainings)))
async def show_trainings(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    locale.setlocale(locale.LC_TIME, LOCALE)
    formatted_date_string = '%A, %d %B'
    if callback_data.target == ClientMainMenuMoveTo.my_trainings:
        trainings = get_client_trainings(tg_id=callback.from_user.id, start_pos=-4, range=4)[0]
        query = MyTrainings(start_pos=trainings['length']-4,
                                                         end_pos=trainings['length']-1,
                                                         length=trainings['length'])
        await state.update_data({'query': query})

    else:
        state_data = await state.get_data()
        query = state_data['query']

        if callback_data.target == MyTrainingsMoveTo.to_prev_trainings:
            query.update(start_pos=query.start_pos-4 if query.start_pos-4 >= 0 else 0,
                         end_pos=query.end_pos - 4)

        elif callback_data.target == MyTrainingsMoveTo.to_next_trainings:
            query.update(start_pos=query.end_pos+1 if query.start_pos < 4 else query.start_pos+4, end_pos=query.end_pos + 4)

        trainings = get_client_trainings(tg_id=callback.from_user.id, start_pos=query.start_pos,
                                         range=query.end_pos+1 if query.end_pos < 4 else 4)[0]

    options = []
    for training in trainings['selected_trainings']:
        options.append(MyTrainingsOption(text=str(training['value']['date'].strftime(formatted_date_string)),
                                         target=ClientMyTrainingsTarget.show_training,
                                         option=str(training['index'])))

    keyboard = PaginationKeyboard(options=options, list_length=query.length,
                                  last_index=query.end_pos,
                                  first_index=query.start_pos,
                                  prev_target=MyTrainingsMoveTo.to_prev_trainings,
                                  next_target=MyTrainingsMoveTo.to_next_trainings,
                                  go_back_target=CommonGoBackMoveTo.to_client_main_menu)
    await callback.message.edit_text(text=f'Выбирай день тренировки', reply_markup=keyboard.as_markup())


@my_trainings_router.callback_query(ChooseCallback.filter(F.target == ClientMyTrainingsTarget.show_training))
async def show_training(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    locale.setlocale(locale.LC_TIME, LOCALE)
    formatted_date_string = '%A, %d %B'
    training_id = int(callback_data.option)
    training = get_client_training(tg_id=callback.from_user.id, training_id=training_id)
    print(training)
    exercises = training['training_exercises']
    await state.update_data({'training_exercises': exercises, 'training_id': training_id})
    await callback.message.edit_text(text=f'Тренировка\nДата: {training.date.strftime(formatted_date_string)}\nУпражнения:',
                                     reply_markup=TrainingExercisesKeyboard(target=ClientMyTrainingsTarget.show_exercise,
                                                                            go_back_target=ClientMainMenuMoveTo.my_trainings,
                                                                            exercises=exercises).as_markup())


@my_trainings_router.callback_query(ChooseCallback.filter(F.target == ClientMyTrainingsTarget.show_exercise))
async def show_training_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    exercise = state_data['training_exercises'][int(callback_data.option)]
    if exercise.video_link != '':
        has_video = True
    else:
        has_video = False
    training_id = state_data['training_id']
    await state.update_data({'selected_exercise': exercise, 'selected_exercise_id': callback_data.option})
    msg_text = f'Упражнение: {exercise.exercise.name}\n' \
               f'Количество: {exercise.num_runs}x{exercise.num_repeats}\n' \
               f'Вес с которым работал: {exercise.weight} кг'
    reply_markup = TrainingSingleExerciseKeyboard(has_video=has_video, target=MyTrainingsMoveTo.show_exercise_video,
                                                  go_back_target=ClientMyTrainingsTarget.show_training,
                                                  source_option=str(training_id)).as_markup()

    if callback.message.video:
        await callback.message.edit_caption(reply_markup=None, caption=callback.message.caption)
        await bot.send_message(chat_id=callback.from_user.id, text=msg_text, reply_markup=reply_markup)
    else:
        await callback.message.edit_text(text=msg_text, reply_markup=reply_markup)

@my_trainings_router.callback_query(MoveCallback.filter(F.target == MyTrainingsMoveTo.show_exercise_video))
async def show_exercise_video(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await  state.get_data()
    exercise = state_data['selected_exercise']
    selected_exercise_id = state_data['selected_exercise_id']
    await callback.answer(text='Загружаю видео')
    exercise_link = create_presigned_url(PHOTO_BUCKET, exercise.video_link)
    r = requests.get(exercise_link)
    filename = exercise.video_link.split('/')[-1].split('.')[0]
    open(f'tmp/{callback.from_user.id}-{filename}.mp4', 'wb').write(r.content)
    print(exercise.video_link)
    print(filename)
    print('downloaded')
    file = FSInputFile(f'tmp/{callback.from_user.id}-{filename}.mp4')

    await bot.send_video(chat_id=callback.from_user.id, video=file,
                         caption=f'{f"Комментарий: {exercise.commnet}" if exercise.comment else "Комментарий отсутствует"}',
                         reply_markup=TrainingVideoKeyboard(go_back_target=ClientMyTrainingsTarget.show_exercise,
                                                            source_option=selected_exercise_id).as_markup())










