from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.callbacks.targets.registration import RegistrationTargets
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, YesNoOptions
from app.bot import bot
from app.callbacks.options.registration import RegistrationOptions
from app.states.registration.states import RegistrationStates
from app.keyboards.yes_no import YesNoKeyboard
from app.entities.single_file.crud import *
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.trainer.utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard
from app.s3.uploader import upload_file
from app.workflows.registration.utils.states import RegisterStates
import os


registration_router = Router()


@registration_router.callback_query(ChooseCallback.filter(F.target == RegistrationTargets.choose_user_type))
async def start_registration_process(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    if 'process_user' in state_data:
        await callback.answer(text='Необходимо закончить текущую регистрацию', show_alert=True)
        await callback.message.delete()
    else:
        await state.update_data({'process_user': True})
        if callback_data.option == RegistrationOptions.trainer:
            if get_client_by_id(tg_id=callback.from_user.id):
                await callback.answer(text='Ты уже зарегистрирован как клиент', show_alert=True)
                await callback.message.delete()
            elif get_trainer(tg_id=callback.from_user.id):
                await callback.answer(text='Ты уже зарегистрирован как тренер', show_alert=True)
                await callback.message.delete()
            else:
                usr_type = RegistrationOptions.trainer
                msg_text = "Привет тренер, введи свое имя"

        elif callback_data.option == RegistrationOptions.client:
            if get_trainer(tg_id=callback.from_user.id):
                await callback.answer(text='Ты уже зарегистрирован как тренер', show_alert=True)
                await callback.message.delete()
            elif get_client_by_id(tg_id=callback.from_user.id):
                await callback.answer(text='Ты уже зарегистрирован как клиент', show_alert=True)
                await callback.message.delete()
            else:
                usr_type = RegistrationOptions.client
                msg_text = "Привет клиент, введи свое имя"

    await state.set_state(RegistrationStates.process_user_name)
    await state.update_data({"usr_type": usr_type})
    await callback.message.edit_text(msg_text)
    await callback.answer()


@registration_router.message(RegistrationStates.process_user_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await state.set_state(RegistrationStates.process_user_surname)
    await message.answer(f'Отлично {message.text}, а теперь введи свою фамилию')


@registration_router.message(RegistrationStates.process_user_surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data({'surname': message.text})
    state_data = await state.get_data()
    print(state_data)
    user_name = state_data['name']
    await state.set_state(RegistrationStates.ask_for_user_photo)
    await message.answer(f'Отлично {user_name}, а хочешь загрузить фото?',
                         reply_markup=YesNoKeyboard(target=RegistrationTargets.process_user_photo).as_markup())


@registration_router.callback_query(ChooseCallback.filter(F.target == RegistrationTargets.process_user_photo))
async def declined_photo_message(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    usr_type = await state.get_data()
    if callback_data.option == YesNoOptions.no:
        await state.update_data({'photo_link': 'defaults/no-user-image-icon-0.png'})

        if usr_type['usr_type'] == RegistrationOptions.client:
            reply_str = 'Хочешь ли то чтобы твой профиль был виден тренерам?'

        elif usr_type['usr_type'] == RegistrationOptions.trainer:
            reply_str = 'Хочешь ли то чтобы твой профиль был виден клиентам?'

        await callback.message.edit_text(reply_str, reply_markup=YesNoKeyboard(target=RegistrationTargets.process_user_visibility).as_markup())
        await state.set_state(RegistrationStates.ask_for_user_visibility)
        await callback.answer()
    elif callback_data.option == YesNoOptions.yes:
        if usr_type['usr_type'] == RegistrationOptions.client:
            await callback.message.edit_text(f'Отлично, тогда пришли мне свое лучшее фото(нюдсы не стоит), чтобы тренера могли его увидеть')

        elif usr_type['usr_type'] == RegistrationOptions.trainer:
            await callback.message.edit_text(f'Отлично, тогда пришли мне свое лучшее фото(нюдсы не стоит), чтобы клиенты могли его увидеть')
        await state.set_state(RegistrationStates.process_user_photo)
        await callback.answer()


@registration_router.message(RegistrationStates.process_user_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    destination = f'tmp/{message.photo[-1].file_id}.jpg'
    await bot.download(message.photo[-1], destination=destination)
    upload_file(file=destination, destination=f'users/{message.from_user.id}/avatar.jpg')
    os.remove(destination)
    await state.update_data({"photo_link": f"users/{message.from_user.id}/avatar.jpg"})
    await state.set_state(RegisterStates.process_visibility)

    user_type = await state.get_data()

    if user_type['usr_type'] == RegistrationOptions.client:
        reply_str = "Cпасибо за фото, теперь скажи, хочешь ли то чтобы твой профиль был виден тренерам?"

    elif user_type['usr_type'] == RegistrationOptions.trainer:
        reply_str = 'Cпасибо за фото, теперь скажи, хочешь ли то чтобы твой профиль был виден клиентам?'
    await state.set_state(RegistrationStates.ask_for_user_visibility)
    await message.answer(reply_str,
                         reply_markup=YesNoKeyboard(target=RegistrationTargets.process_user_visibility).as_markup())


@registration_router.message(RegistrationStates.process_user_photo, F.text)
async def process_photo(message: Message, state: FSMContext):
    await message.answer('Я ожидаю фотографию')


@registration_router.callback_query(ChooseCallback.filter(F.target == RegistrationTargets.process_user_visibility))
async def process_visibility(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(RegistrationStates.process_user_visibility)
    if callback_data.option == YesNoOptions.yes:
        visibility = True

    elif callback_data.option == YesNoOptions.no:
        visibility = False

    await state.update_data({'visibility': visibility})

    await state.set_state(RegistrationStates.process_user_save)
    user_info = await state.get_data()
    if callback.from_user.username:
        username = callback.from_user.username
    else:
        username = None

    if user_info['usr_type'] == RegistrationOptions.client:
        if get_client_by_id(tg_id=callback.from_user.id):
            new_client = get_client_by_id(tg_id=callback.from_user.id)
            new_client.name = user_info['name']
            new_client.surname = user_info['surname']
            new_client.tg_username = username
            new_client.photo_link = user_info['photo_link']
            new_client.visibility = user_info['visibility']
            new_client.save()
        else:
            new_client = Client(tg_id=callback.from_user.id,
                                 name=user_info['name'],
                                 surname=user_info['surname'],
                                 tg_username=username,
                                 photo_link=user_info['photo_link'],
                                 visibility=user_info['visibility'],
                                )
            create_client(new_client)

        await callback.message.edit_text(
            'Добро пожаловать в меню клиента, тут ты можешь добавлять тренировки и просмотривать информацию о уже '
            'добавленных тренировках',
            reply_markup=create_client_main_menu_keyboard(client=new_client))

    elif user_info['usr_type'] == RegistrationOptions.trainer:
        create_trainer(Trainer(tg_id=callback.from_user.id,
                               name=user_info['name'],
                               tg_username=username,
                               surname=user_info['surname'],
                               photo_link=user_info['photo_link'],
                               visibility=user_info['visibility']))
        await callback.message.edit_text('Добро пожаловать в меню тренера, тут ты можешь добавлять тренировки и '
                                         'просмотривать информацию о уже добавленных тренировках',
                                         reply_markup=create_trainer_main_menu_keyboard())

    await state.clear()
    await callback.answer()
