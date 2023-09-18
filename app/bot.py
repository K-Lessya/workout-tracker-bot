import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from .config import BOT_TOKEN, TESTER_ID, TEST_USERS_ID
from app.keyboards.registration.keyboards import ChooseUsrTypeKeyboard
from app.workflows.registration.keyboards.process_user_type import create_choose_user_type_keyboard
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.trainer.utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.workflows.registration.utils.states import RegisterStates
from app.utilities.default_keyboards.tester_keyboard import create_tester_keyboard
from app.entities.single_file.crud import delete_client_or_trainer
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions
from app.utilities.default_callbacks.default_callbacks import TestCallback, TestTasks
from app.states.registration.states import RegistrationStates
from app.callbacks.callbacks import MoveCallback
from app.translations.base_translations import Languages, translations
from app.keyboards.registration.keyboards import ChooseLanguageKeyboard
from app.entities.single_file.crud import get_all_clients, get_all_trainers
bot = Bot(token=BOT_TOKEN)

test_accounts = TEST_USERS_ID.split(' ')
test_ids = list(map(lambda x: int(x), test_accounts))


dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(RegisterStates.ask_for_user_type)
    print(translations)
    if get_client_by_id(tg_id=message.from_user.id):
        client = get_client_by_id(tg_id=message.from_user.id)
        if client.name:
            await state.clear()
            lang = client.lang
            await message.answer(translations[client.lang].main_menu_text.value,
                                 reply_markup=create_client_main_menu_keyboard(client=client, lang=lang))
        else:
            #await state.set_state(RegistrationStates.process_user_name)
            await message.answer("Please choose language",
                                 reply_markup=ChooseLanguageKeyboard().as_markup())
            #await state.update_data({'usr_type': ChooseUsrTypeOptions.client, 'lang': client.lang})
            # await message.answer(translations[client.lang].already_added_client_welcome_message_1
            #                      .value+client.trainer.name
            #                      + client.trainer.surname
            #                      + translations[client.lang].already_added_client_welcome_message_2.value)
    elif get_trainer(tg_id=message.from_user.id):
        await state.clear()
        trainer = get_trainer(tg_id=message.from_user.id)
        lang = trainer.lang
        await message.answer(translations[trainer.lang].main_menu_text.value,
                             reply_markup=create_trainer_main_menu_keyboard(lang=lang))
    else:

        await message.answer("Please choose language",
                             reply_markup=ChooseLanguageKeyboard().as_markup())



@dp.message(RegisterStates.ask_for_user_type)
async def alert(message: types.Message, state: FSMContext):
    # await message.delete()
    state_data = await state.get_data()
    lang = state_data['user_lang']
    await message.reply(text=translations[lang].use_btn_alert.value, reply_markup=create_choose_user_type_keyboard())


@dp.message(Command("tester"))
async def cmd_tester(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == int(TESTER_ID):
        await message.answer(f'{message.from_user.first_name}, Андрей ленивая жопа и добавил только удаление',
                             reply_markup=create_tester_keyboard(testers_id=test_ids))
    else:
        await message.answer('You are not a test user')

@dp.message(Command("switch_role"))
async def switch_role(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == int(TESTER_ID):
        client = get_client_by_id(tg_id=int(TESTER_ID))

        if client:
            print(client)
            client.update(tg_id=23432565)
            trainer = get_trainer(tg_id=23432565)
            trainer.update(tg_id=int(TESTER_ID))
        else:
            trainer = get_trainer(tg_id=int(TESTER_ID))

            if trainer:
                print(trainer)
                trainer.update(tg_id=23432565)
                client = get_client_by_id(tg_id=23432565)
                client.update(tg_id=int(TESTER_ID))

        await message.answer("Роль сменена. Жми start")
    else:
        await message.answer("Эта функция только для тестировщиков. Используйте команду start")

@dp.startup()
async def send_restart_message():
    recievers = TEST_USERS_ID.split(' ')
    for reciever in recievers:
        await bot.send_message(chat_id=int(reciever), text="Я был обновлен до новой версии")


# @dp.startup()
# async def broadcast():
#     clients = get_all_clients()
#     trainers = get_all_trainers()
#     all_users = []
#     for client in clients:
#         all_users.append(client.tg_id)
#     for trainer in trainers:
#         all_users.append(trainer.tg_id)
#     for user in all_users:
#         await bot.send_message(chat_id=user, text="Бот перезапущен после обновления пожалуйста используй комманду start")

@dp.callback_query(TestCallback.filter(F.test_task == TestTasks.delete_me))
async def delete_test_user(callback: CallbackQuery, callback_data: TestCallback, state: FSMContext):
    delete_client_or_trainer(int(callback_data.user))
    await callback.message.edit_text("You was deleted, use /start command again")


@dp.callback_query(MoveCallback.filter(F.target == "to_no_content"))
async def not_added_handler(callback: CallbackQuery, callback_data: str, state: FSMContext):
    await callback.answer(text='Coming soon :)', show_alert=True)


@dp.message(Command("version"))
async def get_version(message: types.Message, state: FSMContext):
    version = os.environ.get("APP_VERSION")
    reply = await message.answer(f"Current version is\n{version}")
    await bot.pin_chat_message(chat_id=message.from_user.id, message_id=reply.message_id, disable_notification=True)
