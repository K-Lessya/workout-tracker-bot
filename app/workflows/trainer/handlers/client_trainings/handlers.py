import locale, requests
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.bot import bot
from app.config import PHOTO_BUCKET, LOCALE
from app.s3.downloader import create_presigned_url
from app.callbacks.callbacks import MoveCallback
from app.entities.single_file.crud import get_client_trainings, get_client_training, get_all_client_trainigs
from app.keyboards.trainings.keyboard import PaginationKeyboard, TrainingExercisesKeyboard,\
    TrainingSingleExerciseKeyboard, TrainingVideoKeyboard
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.workflows.client.classes.my_trainings import MyTrainings, MyTrainingsOption
from app.workflows.trainer.utils.states import TrainerStates
from app.utilities.helpers_functions import callback_error_handler
from app.translations.base_translations import translations
from app.entities.single_file.crud import get_trainer

my_clients_trainings_router = Router()


@my_clients_trainings_router.callback_query(MoveCallback.filter((F.target == MyCLientsMoveTo.show_trainings) |
                                                                (F.target == MyCLientsMoveTo.show_prev_trainings) |
                                                                (F.target == MyCLientsMoveTo.show_next_trainings)))
@callback_error_handler
async def show_client_trainings(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    locale.setlocale(locale.LC_TIME, LOCALE)
    formatted_date_string = '%d %m %Y'
    state_data = await state.get_data()
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    await state.update_data({'lang': lang})
    await state.set_state(TrainerStates.my_clients.client_training.working_with_menu)
    client = state_data['client']
    if callback_data.target == MyCLientsMoveTo.show_trainings:
        trainings = get_client_trainings(tg_id=client.tg_id, start_pos=-4, range=4)[0]
        all_trainings = get_all_client_trainigs(tg_id=client.tg_id)
        if trainings != []:
            query = MyTrainings(start_pos=trainings['length']-4,
                                end_pos=trainings['length']-1,
                                length=trainings['length'])
            await state.update_data({'query': query})
        else:
            await callback.answer(translations[lang].trainer_my_clients_menu_single_client_view_trainings_no_trainings
                                  .value,
                                  show_alert=True
                                  )
            pass
    else:

        query = state_data['query']
        if callback_data.target == MyCLientsMoveTo.show_prev_trainings:
            query.update(start_pos=query.start_pos-4 if query.start_pos-4 >= 0 else 0,
                         end_pos=query.end_pos - 4)
        elif callback_data.target == MyCLientsMoveTo.show_next_trainings:
            query.update(start_pos=query.end_pos+1 if query.start_pos < 4 else query.start_pos+4,
                         end_pos=query.end_pos + 4)

        trainings = get_client_trainings(tg_id=client.tg_id, start_pos=query.start_pos,
                                         range=query.end_pos+1 if query.end_pos < 4 else 4)[0]
    options = []
    if trainings:
        print(trainings['selected_trainings'])
        if trainings['selected_trainings']:
            for training in trainings['selected_trainings']:
                options.append(MyTrainingsOption(text=f'{training["value"]["name"]} '
                                                      f'({str(training["value"]["date"].strftime(formatted_date_string))})',
                                                 target=TrainerMyClientsTargets.show_training,
                                                 option=str(training['index'])))

            keyboard = PaginationKeyboard(options=options, list_length=query.length,
                                          last_index=query.end_pos,
                                          lang=lang,
                                          first_index=query.start_pos,
                                          prev_target=MyCLientsMoveTo.show_prev_trainings,
                                          next_target=MyCLientsMoveTo.show_next_trainings,
                                          go_back_to_choose=True,
                                          choose_option=str(client.id),
                                          go_back_target=TrainerMyClientsTargets.show_client)
            if callback.message.photo:
                await callback.message.delete()
                await bot.send_message(chat_id=callback.from_user.id,
                                       text=translations[lang]
                                       .trainer_my_clients_menu_single_client_view_trainings_choose_day.value,
                                       reply_markup=keyboard.as_markup())
            else:
                await callback.message.edit_text(text=translations[lang]
                                                 .trainer_my_clients_menu_single_client_view_trainings_choose_day.value,
                                                 reply_markup=keyboard.as_markup())


@my_clients_trainings_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_training))
@callback_error_handler
async def show_client_single_training(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    locale.setlocale(locale.LC_TIME, LOCALE)
    formatted_date_string = '%d/%m/%Y'
    state_data = await state.get_data()
    client = state_data['client']
    lang = state_data['lang']
    training_id = int(callback_data.option)
    training = get_client_training(tg_id=client.tg_id, training_id=training_id)
    training_name = training.name
    exercises = training['training_exercises']
    await state.update_data({'training_exercises': exercises, 'training_id': training_id})
    await callback.message.edit_text(
        text=translations[lang].trainer_my_clients_menu_single_client_view_trainings_show_training
            .value.format(training_name, training.date.strftime(formatted_date_string)),
        reply_markup=TrainingExercisesKeyboard(target=TrainerMyClientsTargets.show_training_exercise,
                                               go_back_target=MyCLientsMoveTo.show_trainings,
                                               exercises=exercises,
                                               lang=lang).as_markup())

@my_clients_trainings_router.callback_query(ChooseCallback.filter(F.target == TrainerMyClientsTargets.show_training_exercise))
@callback_error_handler
async def show_client_training_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    exercise = state_data['training_exercises'][int(callback_data.option)]
    if exercise.video_link != '':
        has_video = True
    else:
        has_video = False
    training_id = state_data['training_id']
    await state.update_data({'selected_exercise': exercise,
                             'selected_exercise_id': callback_data.option})
    msg_text = translations[lang].trainer_my_clients_menu_single_client_view_trainings_show_exercise.value.format(exercise.exercise.name, exercise.num_runs, exercise.num_repeats, exercise.weight)
    reply_markup = TrainingSingleExerciseKeyboard(has_video=has_video,
                                                  target=MyCLientsMoveTo.show_exercise_video,
                                                  go_back_target=TrainerMyClientsTargets.show_training,
                                                  source_option=str(training_id),
                                                  lang=lang).as_markup()
    if callback.message.video:
        await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id, text=msg_text, reply_markup=reply_markup)
    else:
        await callback.message.edit_text(text=msg_text, reply_markup=reply_markup)


@my_clients_trainings_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.show_exercise_video))
@callback_error_handler
async def show_exercise_video(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['lang']
    exercise = state_data['selected_exercise']
    selected_exercise_id = state_data['selected_exercise_id']
    await callback.message.delete()
    notification = await callback.message.answer(text=translations[lang].trainer_my_clients_menu_single_client_view_plan_send_video.value)
    exercise_link = create_presigned_url(PHOTO_BUCKET, exercise.video_link)
    r = requests.get(exercise_link)
    filename = exercise.video_link.split('/')[-1].split('.')[0]
    open(f'tmp/{callback.from_user.id}-{filename}.mp4', 'wb').write(r.content)
    file = FSInputFile(f'tmp/{callback.from_user.id}-{filename}.mp4')

    keyboard = TrainingVideoKeyboard(go_back_target=TrainerMyClientsTargets.show_training_exercise,
                                     source_option=selected_exercise_id, lang=lang)
    keyboard.row(InlineKeyboardButton(text=translations[lang]
                                      .trainer_my_clients_menu_single_client_view_trainings_update_comment
                                      .value if exercise.comment else translations[lang]
                                      .trainer_my_clients_menu_single_client_view_trainings_create_comment.value,
                                      callback_data=MoveCallback(target=MyCLientsMoveTo.create_video_comment).pack()))


    await bot.send_video(chat_id=callback.from_user.id, video=file,
                         caption=translations[lang]
                         .trainer_my_clients_menu_single_client_view_trainings_show_exercise_video
                         .value.format(
                             exercise.client_note,
                             exercise.comment)
                         if exercise.comment else translations[lang]
                         .trainer_my_clients_menu_single_client_view_trainings_show_exercise_video_no_comment
                         .value.format(exercise.client_note),
                         reply_markup=keyboard.as_markup())
    await notification.delete()

@my_clients_trainings_router.callback_query(MoveCallback.filter(F.target == MyCLientsMoveTo.create_video_comment))
@callback_error_handler
async def create_comment(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    await state.set_state(TrainerStates.my_clients.client_training.process_comment)
    state_data = await state.get_data()
    lang = state_data['lang']
    await callback.message.edit_caption(
        caption=translations[lang]
        .trainer_my_clients_menu_single_client_view_trainings_show_exercise_as_for_comment.value,
        reply_markup=None)


@my_clients_trainings_router.message(TrainerStates.my_clients.client_training.process_comment)
async def process_comment(message: Message, state: FSMContext):
    state_data = await state.get_data()
    has_video = True
    client = state_data['client']
    lang = state_data['lang']
    training_id = state_data['training_id']
    selected_exercise_id = state_data['selected_exercise_id']
    client.trainings[int(training_id)].training_exercises[int(selected_exercise_id)].comment = message.text
    await state.update_data({'selected_exercise': client.trainings[int(training_id)].training_exercises[int(selected_exercise_id)]})
    client.save()
    await state.set_state(TrainerStates.my_clients.client_training.working_with_menu)
    await message.answer(text=translations[lang]
                         .trainer_my_clients_menu_single_client_view_trainings_show_exercise_comment_saved.value,
                         reply_markup=TrainingSingleExerciseKeyboard(has_video=has_video,
                                                                     target=MyCLientsMoveTo.show_exercise_video,
                                                                     go_back_target=TrainerMyClientsTargets.show_training,
                                                                     source_option=str(training_id),
                                                                     lang=lang).as_markup())



