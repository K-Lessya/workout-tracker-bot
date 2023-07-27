from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from .config import BOT_TOKEN, TESTER_ID
from app.workflows.registration.keyboards.process_user_type import create_choose_user_type_keyboard
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.trainer.utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.workflows.registration.utils.states import RegisterStates
from app.utilities.default_keyboards.tester_keyboard import create_tester_keyboard
from app.entities.single_file.crud import delete_client_or_trainer
#from app.workflows.registration.handlers import registration_router
from app.utilities.default_callbacks.default_callbacks import TestCallback, TestTasks
bot = Bot(token=BOT_TOKEN)




dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if get_client_by_id(tg_id=message.from_user.id):
        client = get_client_by_id(tg_id=message.from_user.id)
        if client.name:
            await message.answer(f'Привет снова, выбирай, создать тренировку или просмотреть уже созданные',
                                 reply_markup=create_client_main_menu_keyboard(client=client))
        else:
            state.set_state(RegisterStates.process_name)
            await message.answer(f'Привет ты был добавлен в систему тренером {client.trainer.name}',
                                 f'{client.trainer.surname}, давай заполним твой профиль, введи свое имя')
    elif get_trainer(tg_id=message.from_user.id):
        trainer = get_trainer(tg_id=message.from_user.id)
        await message.answer(f'Привет снова, {trainer.name}! Давай продолжим работу, выбери один из пунктов меню',
                             reply_markup=create_trainer_main_menu_keyboard())
    else:
        await message.answer("Привет, регаемся как тренер или как клиент?", reply_markup=create_choose_user_type_keyboard())



@dp.message(Command("tester"))
async def cmd_tester(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == int(TESTER_ID):
        await message.answer(f'{message.from_user.first_name}, Андрей ленивая жопа и добавил только удаление',
                             reply_markup=create_tester_keyboard())
    else:
        await message.answer('You are not a test user')


@dp.callback_query(TestCallback.filter(F.test_task == TestTasks.delete_me))
async def delete_test_user(callback: CallbackQuery, callback_data: TestCallback, state: FSMContext):
    delete_client_or_trainer(callback.from_user.id)
    await callback.message.edit_text("You was deleted, use /start command again")