import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from .config import BOT_TOKEN
from app.workflows.registration.keyboards.choose_user import create_choose_user_type_keyboard
from app.entities.single_file.crud import get_client_by_id, get_trainer
#from app.workflows.registration.handlers import registration_router

bot = Bot(token=BOT_TOKEN)




dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if get_client_by_id(tg_id=message.from_user.id):
        await message.answer(f'Привет {get_client_by_id(tg_id=message.from_user.id).name}, ты клиент')
    elif get_trainer(tg_id=message.from_user.id):
        await message.answer(f'Привет {get_client_by_id(tg_id=message.from_user.id).name}, ты тренер')
    else:
        await message.answer("Привет, регаемся как тренер или как клиент?", reply_markup=create_choose_user_type_keyboard())
