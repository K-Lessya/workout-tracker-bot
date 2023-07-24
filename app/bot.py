from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from .config import BOT_TOKEN
from app.workflows.registration.keyboards.process_user_type import create_choose_user_type_keyboard
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.trainer.utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.workflows.registration.utils.states import RegisterStates

#from app.workflows.registration.handlers import registration_router

bot = Bot(token=BOT_TOKEN)




dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if get_client_by_id(tg_id=message.from_user.id):
        client = get_client_by_id(tg_id=message.from_user.id)
        if client.name:
            await message.answer(f'Привет снова, выбирай, создать тренировку или просмотреть уже созданные',
                                 reply_markup=create_client_main_menu_keyboard())
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


@dp.message(Command("admin"))
async def cmd_start(message: types.Message):
    if get_client_by_id(tg_id=message.from_user.id):
        await message.answer(f'Привет {get_client_by_id(tg_id=message.from_user.id).name}, ты клиент')
    elif get_trainer(tg_id=message.from_user.id):
        await message.answer(f'Привет {get_trainer(tg_id=message.from_user.id).name}, ты тренер')
    else:
        await message.answer("Привет, регаемся как тренер или как клиент?", reply_markup=create_choose_user_type_keyboard())