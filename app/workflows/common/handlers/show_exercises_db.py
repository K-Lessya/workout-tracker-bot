import requests
from aiogram import Router
from aiogram import F
from app.bot import bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, URLInputFile, Message

from app.keyboards.yes_no import YesNoKeyboard
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard
from app.workflows.common.utils.callback_properties.movetos import UpstreamMenuMoveTo, CommonGoBackMoveTo
from app.workflows.common.utils.callback_properties.targets import ExerciseDbTargets
from app.workflows.common.utils.keyboards.exercise_db_choose import create_exercise_db_choose_keyboard
from ..utils.callback_properties.targets import ExerciseDbTargets
from app.entities.exercise.crud import *
from app.s3.downloader import create_presigned_url
from app.config import PHOTO_BUCKET
from app.utilities.helpers_functions import callback_error_handler
from app.entities.single_file.crud import get_trainer
from app.workflows.trainer.utils.states import TrainerStates
from ...trainer.utils.callback_properties.targets import CreateExerciseTargets
from app.translations.base_translations import translations

show_exercises_db_router = Router()

@show_exercises_db_router.callback_query(MoveToCallback.filter(F.move_to == UpstreamMenuMoveTo.show_exercise_db))
@callback_error_handler
async def list_body_parts(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    trainer =get_trainer(callback.from_user.id)
    lang = trainer.lang
    await state.update_data({'lang': lang})

    body_parts = get_all_body_parts(trainer)
    await state.set_state(TrainerStates.exercises_db.process_buttons.choose_body_part)
    await callback.message.edit_text(translations[lang].trainer_exercise_db_menu_choose_body_part.value,
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=body_parts,
                                         source=callback,
                                         target=ExerciseDbTargets.show_body_part,
                                         go_back_filter=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu),
                                         lang=lang
                                     ))
    await callback.answer()

@show_exercises_db_router.callback_query(ChooseCallback.filter(F.target == ExerciseDbTargets.show_body_part))
@callback_error_handler
async def show_muscle_groups(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    body_part = get_body_part_by_id(callback_data.option)
    trainer = get_trainer(callback.from_user.id)
    await state.update_data({'lang': trainer.lang})
    state_data = await state.get_data()
    lang = state_data['lang']
    await state.set_state(TrainerStates.exercises_db.process_buttons.choose_muscle_group)
    await state.update_data({'body_part': body_part})
    muscle_groups = get_muscle_groups_by_body_part(body_part=body_part.id)
    await callback.message.edit_text(translations[lang].trainer_exercise_db_menu_choose_muscle_group.value,
                                     reply_markup=create_exercise_db_choose_keyboard(
                                         options=muscle_groups,
                                         source=callback,
                                         target=ExerciseDbTargets.show_muscle_group,
                                         go_back_filter=MoveToCallback(move_to=UpstreamMenuMoveTo.show_exercise_db),
                                         lang=lang
                                     ))
    await callback.answer()

@show_exercises_db_router.callback_query(ChooseCallback.filter(F.target == ExerciseDbTargets.show_muscle_group))
@callback_error_handler
async def show_muscle_groups(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    muscle_group = get_muscle_group_by_id(callback_data.option)
    await state.set_state(TrainerStates.exercises_db.process_buttons.choose_exercise)
    state_data = await state.get_data()
    lang = state_data['lang']
    go_back_ref = str(state_data['body_part'].id)
    print(muscle_group)
    exercises = get_exercises_by_muscle_group(muscle_group=muscle_group.id)
    await state.update_data({'muscle_group': muscle_group})
    print(exercises)
    if 'has_media' in state_data.keys():
        await bot.send_message(chat_id=callback.from_user.id,
                               text=translations[lang].trainer_exercise_db_menu_choose_exercise.value,
                               reply_markup=create_exercise_db_choose_keyboard(
                                   options=exercises,
                                   source=callback,
                                   target=ExerciseDbTargets.show_exercise,
                                   go_back_filter=ChooseCallback(target=ExerciseDbTargets.show_body_part,
                                                                 option=go_back_ref),
                                   lang=lang
                               ))
        await callback.message.delete()
    else:
        await callback.message.edit_text(translations[lang].trainer_exercise_db_menu_choose_exercise.value,
                                         reply_markup=create_exercise_db_choose_keyboard(
                                             options=exercises,
                                             source=callback,
                                             target=ExerciseDbTargets.show_exercise,
                                             go_back_filter=ChooseCallback(target=ExerciseDbTargets.show_body_part,
                                                                           option=go_back_ref),
                                             lang=lang
                                         ))
    await callback.answer()


@show_exercises_db_router.callback_query(ChooseCallback.filter(F.target == ExerciseDbTargets.show_exercise))
@callback_error_handler
async def show_exercise(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    exercise = get_exercise_by_id(callback_data.option)
    state_data = await state.get_data()
    lang = state_data['lang']
    await callback.message.edit_text(translations[lang].trainer_exercise_db_menu_sending_exercie_media.value)
    await callback.answer()
    print(exercise.media_link)
    media_link = create_presigned_url(PHOTO_BUCKET, exercise.media_link)
    print(media_link)
    go_back_ref = str(state_data['muscle_group'].id)
    keyboard = create_exercise_db_choose_keyboard(
                                 options=None,
                                 source=callback,
                                 target="Exercise",
                                 lang=lang,
                                 go_back_filter=ChooseCallback(target=ExerciseDbTargets.show_muscle_group,
                                                               option=go_back_ref))

    if exercise.media_type == 'photo':
        await state.update_data({'has_media': True})
        await bot.send_photo(chat_id=callback.from_user.id, photo=media_link,
                             caption=f"{exercise.name}",
                             reply_markup=keyboard)
    elif exercise.media_type == 'video':
        await state.update_data({'has_media': True})

        file = URLInputFile(url=media_link, bot=bot)
        print(file)
        await bot.send_video(chat_id=callback.from_user.id, video=file,
                             caption=f'{exercise.name}',
                             reply_markup=keyboard)
    await callback.message.delete()



@show_exercises_db_router.message(TrainerStates.exercises_db.process_buttons.choose_body_part)
async def process_buttons_body_part_message(message: Message, state: FSMContext):
    await state.update_data({'body_part': message.text})
    state_data = await state.get_data()
    lang = state_data['lang']
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_muscle_group_name)
    await message.answer(translations[lang].trainer_exercise_db_menu_inline_create_body_part.value.format(message.text))

@show_exercises_db_router.message(TrainerStates.exercises_db.process_buttons.choose_muscle_group)
async def process_buttons_muscle_group_message(message: Message, state: FSMContext):
    await state.update_data({'muscle_group': message.text})
    state_data = await state.get_data()
    lang = state_data['lang']
    body_part = state_data['body_part']
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_exercise_name)
    await message.answer(translations[lang].trainer_exercise_db_menu_inline_create_muscle_group
                         .value.format(body_part.name, message.text))


@show_exercises_db_router.message(TrainerStates.exercises_db.process_buttons.choose_exercise)
async def process_buttons_exercise_message(message: Message, state: FSMContext):
    await state.update_data({'exercise_name': message.text, 'file_recieved': False})
    state_data = await state.get_data()
    lang = state_data['lang']
    await state.set_state(TrainerStates.exercises_db.add_exercise.process_photo)
    await message.answer(translations[lang].trainer_exercise_db_menu_inline_create_exercise.value,
                         reply_markup=YesNoKeyboard(
                             target=CreateExerciseTargets.ask_for_exercise_photo,
                             lang=lang).as_markup())










