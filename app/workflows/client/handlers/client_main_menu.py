import os
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram import F
from app.bot import bot
from app.s3.downloader import create_presigned_url
from aiogram.fsm.context import FSMContext
from app.config import PHOTO_BUCKET
from app.utilities.default_callbacks.default_callbacks import MoveToCallback, ChooseCallback
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard
from app.utilities.default_callbacks.default_callbacks import YesNoOptions
from ..utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.entities.single_file.crud import *
from ..utils.keyboards.client_requests_list import create_client_income_requests_keyboard
from ..utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from ..utils.callback_properties.targets import ClientIncomeRequestTargets
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo



client_main_menu_router = Router()


@client_main_menu_router.callback_query(MoveToCallback.filter(F.move_to == CommonGoBackMoveTo.to_client_main_menu))
async def show_client_main_menu(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    await state.clear()
    client = get_client_by_id(tg_id=callback.from_user.id)
    await bot.send_message(chat_id=callback.from_user.id, text='Меню клиента',
                           reply_markup=create_client_main_menu_keyboard(client=client))
    await callback.message.delete()
    await callback.answer()