from aiogram import Router
from aiogram.types import URLInputFile, CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.utilities.callback_types import ChooseCallback, ChooseCallbackOptions, ChooseCallbackTargets, YesNoOptions,\
    SeePhotoCallback, SeePhotoActions
from app.bot import bot
from app.entities.single_file.models import Client, Trainer
from app.entities.single_file.crud import create_client, create_trainer
from app.workflows.client.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.s3.uploader import upload_file
from app.s3.downloader import create_presigned_url
from app.config import PHOTO_BUCKET
from .keyboards.process_photo import create_yes_no_keyboard
from .keyboards.temporary import create_see_photo_keyboard
from .utils.states import RegisterStates
import os




registration_router = Router()  # [1]


@registration_router.callback_query(ChooseCallback.filter(F.target == ChooseCallbackTargets.usr_type))
async def start_registration_process(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == ChooseCallbackOptions.trainer:
        usr_type = ChooseCallbackOptions.trainer
        msg_text = "Привет тренер, введи свое имя"

    elif callback_data.option == ChooseCallbackOptions.client:
        usr_type = ChooseCallbackOptions.client
        msg_text = "Привет клиент, введи свое имя"

    await state.set_state(RegisterStates.process_name)
    await state.update_data({"usr_type": usr_type})
    await callback.message.edit_text(msg_text)
    await callback.answer()


@registration_router.message(RegisterStates.process_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await state.set_state(RegisterStates.process_surname)
    await message.answer(f'Отлично {message.text}, а теперь введи свою фамилию')


@registration_router.message(RegisterStates.process_surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data({'surname': message.text})
    await state.set_state(RegisterStates.process_photo)
    await message.answer(f'Отлично {message.text}, а хочешь загрузить фото?',
                         reply_markup=create_yes_no_keyboard(target=ChooseCallbackTargets.process_photo))


@registration_router.callback_query(ChooseCallback.filter(F.target == ChooseCallbackTargets.process_photo),
                                    ChooseCallback.filter(F.option == YesNoOptions.no))
async def declined_photo_message(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    usr_type = await state.get_data()

    await state.update_data({'photo_link': None})

    if usr_type['usr_type'] == ChooseCallbackOptions.client:
        reply_str = 'Хочешь ли то чтобы твой профиль был виден тренерам?'

    elif usr_type['usr_type'] == ChooseCallbackOptions.trainer:
        reply_str = 'Хочешь ли то чтобы твой профиль был виден клиентам?'

    await callback.message.edit_text(reply_str, reply_markup=create_yes_no_keyboard(target=ChooseCallbackTargets.process_visibility))
    await state.set_state(RegisterStates.process_visibility)
    await callback.answer()


@registration_router.callback_query(ChooseCallback.filter(F.target == ChooseCallbackTargets.process_photo),
                                    ChooseCallback.filter(F.option == YesNoOptions.yes))
async def process_photo_message(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    user_type = await state.get_data()

    if user_type['usr_type'] == ChooseCallbackOptions.client:
        await callback.message.edit_text(f'Отлично, тогда пришли мне свое лучшее фото(нюдсы не стоит), чтобы тренера могли его увидеть')

    elif user_type['usr_type'] == ChooseCallbackOptions.trainer:
        await callback.message.edit_text(f'Отлично, тогда пришли мне свое лучшее фото(нюдсы не стоит), чтобы клиенты могли его увидеть')
    await callback.answer()


@registration_router.message(RegisterStates.process_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    destination = f'tmp/{message.photo[-1].file_id}.jpg'

    await bot.download(message.photo[-1], destination=destination)
    upload_file(file=destination, destination=f'users/{message.from_user.id}/avatar.jpg')
    os.remove(destination)
    await state.update_data({"photo_link": f"users/{message.from_user.id}/avatar.jpg"})
    await state.set_state(RegisterStates.process_visibility)

    user_type = await state.get_data()

    if user_type['usr_type'] == ChooseCallbackOptions.client:
        reply_str = "Cпасибо за фото, теперь скажи, хочешь ли то чтобы твой профиль был виден тренерам?"

    elif user_type['usr_type'] == ChooseCallbackOptions.trainer:
        reply_str = 'Cпасибо за фото, теперь скажи, хочешь ли то чтобы твой профиль был виден клиентам?'
    await message.answer(reply_str,
                         reply_markup=create_yes_no_keyboard(target=ChooseCallbackTargets.process_visibility))


@registration_router.message(RegisterStates.process_photo, F.text)
async def process_photo(message: Message, state: FSMContext):
    await message.answer('Я ожидаю фотографию')


@registration_router.callback_query(ChooseCallback.filter(F.target == ChooseCallbackTargets.process_visibility))
async def process_visibility(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == YesNoOptions.yes:
        visibility = True
        user_visibility = 'Да'

    elif callback_data.option == YesNoOptions.no:
        visibility = False
        user_visibility = 'Нет'

    await state.update_data({'visibility': visibility})

    user_info = await state.get_data()
    if callback.from_user.username:
        username = callback.from_user.username
    else:
        username = None
    if user_info['usr_type'] == ChooseCallbackOptions.client:
        user_type = 'Клиент'
        create_client(Client(tg_id=callback.from_user.id,
                             name=user_info['name'],
                             surname=user_info['surname'],
                             tg_username=username,
                             photo_link=user_info['photo_link'],
                             visibility=user_info['visibility']))

    elif user_info['usr_type'] == ChooseCallbackOptions.trainer:
        user_type = 'Тренер'
        create_trainer(Trainer(tg_id=callback.from_user.id,
                               name=user_info['name'],
                               tg_username=username,
                               surname=user_info['surname'],
                               photo_link=user_info['photo_link'],
                               visibility=user_info['visibility']))
    if user_info['usr_type'] == 'trainer':
        if user_info['photo_link'] == None:
            await callback.message.edit_text(f'Настройка сохранена\nДавай проверим твои данные:\nИмя: {user_info["name"]}\nФамилия: {user_info["surname"]}\nТип пользователя: {user_type}\nВидимость другим: {user_visibility}',
                                     )
        else:
            await callback.message.edit_text(
            f'Настройка сохранена\nДавай проверим твои данные:\nИмя: {user_info["name"]}\nФамилия: {user_info["surname"]}\nТип пользователя: {user_type}\nВидимость другим: {user_visibility}',
            reply_markup=create_see_photo_keyboard())
    elif user_info['usr_type'] == 'client':
        await callback.message.edit_text('Добро пожаловать в меню клиента, тут ты можешь добавлять тренировки и просмотривать информацию о уже добавленных тренировках', reply_markup=create_client_main_menu_keyboard())
    await state.clear()
    await callback.answer()


@registration_router.callback_query(SeePhotoCallback.filter(F.action == SeePhotoActions.see_photo))
async def send_avatar(callback: CallbackQuery, callback_data: SeePhotoCallback, state: FSMContext):
    user_id = callback.from_user.id
    image_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=f'users/{user_id}/avatar.jpg',
                                      expiration=3600)
    image_from_url = URLInputFile(bot=bot, url=image_link)
    result = await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=image_from_url,
        caption="Твое фото"
    )
