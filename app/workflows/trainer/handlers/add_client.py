from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.bot import bot
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback, YesNoOptions
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard
from ..utils.keyboards.add_client_options import create_add_client_options_keyboard
from ..utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard
from ..utils.keyboards.choose_existing_clients import create_choose_existing_clients_keyboard
from ..utils.states import TrainerStates
from app.workflows.common.utils.callback_properties.movetos import AddClientMoveTo, CommonGoBackMoveTo
from ..utils.callback_properties.movetos import TrainerMainMenuMoveTo
from ..utils.callback_properties.targets import TrainerAddClientTargets
from app.config import PHOTO_BUCKET
from app.utilities.helpers_functions import check_link
from app.entities.single_file.crud import *
from app.s3.downloader import create_presigned_url
from app.workflows.client.utils.keyboards.notifications import create_new_trainer_request_keyboard
from aiogram.types.menu_button_commands import MenuButtonCommands
from app.utilities.helpers_functions import callback_error_handler

add_client_router = Router()

@add_client_router.callback_query(MoveToCallback.filter(F.move_to == TrainerMainMenuMoveTo.add_client))
@callback_error_handler
async def choose_add_flow(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.edit_text(f'Выбери как ты хочешь добавить клиента из списка',
                                     reply_markup=create_add_client_options_keyboard())
    await callback.answer("Загрузка завершена")


@add_client_router.callback_query(MoveToCallback.filter(F.move_to == AddClientMoveTo.by_contact))
@callback_error_handler
async def start_add_client(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(TrainerStates.add_client.process_contact)
    await callback.message.edit_text(f'Для того чтобы добавить клиента, поделись его контактом со мной')
    await callback.answer("Загрузка завершена")


@add_client_router.message(TrainerStates.add_client.process_contact)
async def process_client_contact(message: Message, state: FSMContext):
    if get_trainer(message.contact.user_id):
        await message.answer(f'Этот человек зарегистрирован как тренер, ты не можешь доавить его как клиента',
                             reply_markup=create_trainer_main_menu_keyboard())
        await state.clear()
    else:
        if get_client_by_id(message.contact.user_id):
            client = get_client_by_id(message.contact.user_id)
            if client.trainer:
                if client.trainer.tg_id == message.from_user.id:
                    await message.answer(f'У тебя уже есть такой клиент', reply_markup=create_trainer_main_menu_keyboard())
                else:
                    await message.answer(f'Этот клиент уже занят', reply_markup=create_trainer_main_menu_keyboard())
            else:
                trainer = get_trainer(tg_id=message.from_user.id)
                update_client_trainer(client=client, trainer=trainer)
        else:
            create_client(Client(tg_id=message.contact.user_id, phone_number=message.contact.phone_number,
                                 trainer=get_trainer(message.from_user.id)))
            await state.clear()
            await message.answer(f'Клиент добавлен', reply_markup=create_trainer_main_menu_keyboard())

@add_client_router.callback_query(MoveToCallback.filter(F.move_to == AddClientMoveTo.by_username))
@callback_error_handler
async def start_add_client(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(TrainerStates.add_client.process_username)
    await callback.message.edit_text(f'Для того чтобы добавить клиента, пришли мне ссылку на него')
    await callback.answer("Загрузка завершена")


@add_client_router.message(TrainerStates.add_client.process_username)
async def process_client_contact(message: Message, state: FSMContext):
    if check_link(message.text):
        tg_username = message.text.replace('https://t.me/', '')
        if get_trainer_by_username(tg_username=tg_username):
            await message.answer(f'Этот человек зарегистрирован как тренер, ты не можешь доавить его как клиента',
                                 reply_markup=create_trainer_main_menu_keyboard())
            await state.clear()
        else:
            if get_client_by_username(tg_username=tg_username):
                client = get_client_by_username(tg_username=tg_username)
                if client.trainer:
                    if client.trainer.tg_id == message.from_user.id:
                        await message.answer(f'У тебя уже есть такой клиент', reply_markup=create_trainer_main_menu_keyboard())
                    else:
                        await message.answer(f'Этот клиент уже занят', reply_markup=create_trainer_main_menu_keyboard())
                else:
                    trainer = get_trainer(tg_id=message.from_user.id)
                    update_client_trainer(client=client, trainer=trainer)
            else:
                create_client(Client(tg_username=tg_username))
                await state.clear()
                await message.answer(f'Клиент добавлен', reply_markup=create_trainer_main_menu_keyboard())
    else:
        await message.answer("Это неверная ссылка")

@add_client_router.callback_query(MoveToCallback.filter(F.move_to == AddClientMoveTo.by_existing))
@callback_error_handler
async def add_client_by_existing(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    clients = get_all_not_assigned_clients_with_name()
    print(clients)
    if clients:
        await callback.message.edit_text(f'Выбери клиента из списка',
                                         reply_markup=create_choose_existing_clients_keyboard(clients=clients))
    else:
        await callback.answer(f'Все доступные клиенты уже заняты', show_alert=True)

    await callback.answer("Загрузка завершена")


@add_client_router.callback_query(ChooseCallback.filter(F.target == TrainerAddClientTargets.show_clients))
@callback_error_handler
async def show_user_profile(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    client = get_client_by_id(int(callback_data.option))
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=client.photo_link)
    await state.update_data({'tg_id': client.tg_id})
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link, caption=f'Имя: {client.name}\nФамилия: {client.surname}\nДобавить этого клиента?',
                         reply_markup=create_yes_no_keyboard(target=TrainerAddClientTargets.add_existing_client))
    await callback.message.delete()
    await callback.answer("Загрузка завершена")


@add_client_router.callback_query(ChooseCallback.filter(F.target == TrainerAddClientTargets.add_existing_client))
@callback_error_handler
async def add_client_profile(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == YesNoOptions.yes:
        state_data = await state.get_data()
        client_id = state_data['tg_id']
        client = get_client_by_id(client_id)
        trainer = get_trainer(callback.from_user.id)
        client_add_new_trainer_request(client, trainer)
        await state.clear()
        await bot.send_message(chat_id=callback.from_user.id, text='Клиенту отправлена заявка',
                               reply_markup=create_trainer_main_menu_keyboard())
        await bot.send_message(chat_id=client_id, text='Тебе поступило новое предложение от тренера, посмотри его',
                               reply_markup=create_new_trainer_request_keyboard(str(trainer.id)))
        await callback.message.delete()
    elif callback_data.option == YesNoOptions.no:
        clients = get_all_not_assigned_clients_with_name()
        await state.clear()
        await bot.send_message(chat_id=callback.from_user.id, text=f'Хорошо, посмотрим других',
                               reply_markup=create_choose_existing_clients_keyboard(clients))
        await callback.message.delete()
    await callback.answer("Загрузка завершена")

@add_client_router.callback_query(MoveToCallback.filter(F.move_to == CommonGoBackMoveTo.to_trainer_main_menu))
@callback_error_handler
async def go_to_main_menu(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.edit_text('Мы снова в главном меню',
                                     reply_markup=create_trainer_main_menu_keyboard())
    await bot.set_chat_menu_button(chat_id=callback.from_user.id, menu_button=MenuButtonCommands(type='commands'))
    await callback.answer("Загрузка завершена")

