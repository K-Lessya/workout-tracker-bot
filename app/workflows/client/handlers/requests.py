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
from app.callbacks.callbacks import MoveCallback
from app.utilities.helpers_functions import callback_error_handler

client_request_router = Router()

@client_request_router.callback_query(MoveCallback.filter(F.target == ClientMainMenuMoveTo.my_recieved_requests))
@callback_error_handler
async def show_requests(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    await state.clear()
    client_requests = get_client_requests_by_id(tg_id=callback.from_user.id)
    await callback.message.edit_text('Входящие заявки от тренеров',
                                     reply_markup=create_client_income_requests_keyboard(options=client_requests,
                                         target=ClientIncomeRequestTargets.show_income_request,
                                         go_back_filter=MoveCallback(target=CommonGoBackMoveTo.to_client_main_menu)))
@client_request_router.callback_query(ChooseCallback.filter(F.target == ClientIncomeRequestTargets.show_income_request))
@callback_error_handler
async def show_income_request(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    trainer = get_trainer_by_obj_id(obj_id=callback_data.option)
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET,object_name=trainer.photo_link)
    await state.update_data({'trainer': trainer})
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                         caption=f'Заявка от тренера:\n{trainer.name} {trainer.surname}\nПринять заявку?',
                         reply_markup=create_yes_no_keyboard(target=ClientIncomeRequestTargets.process_income_request))
    await callback.message.delete()
@client_request_router.callback_query(ChooseCallback.filter(F.target == ClientIncomeRequestTargets.process_income_request))
@callback_error_handler
async def process_income_request(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    trainer = state_data['trainer']
    if callback_data.option == YesNoOptions.yes:
        client = get_client_by_id(tg_id=callback.from_user.id)
        update_client_trainer(client=client, trainer=trainer)
        client_delete_trainer_request(client=client, trainer=trainer)
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"Поздравляю, теперь {trainer.name} {trainer.surname} тренирует тебя",
                               reply_markup=create_client_main_menu_keyboard(client=client))

        await bot.send_message(chat_id=trainer.tg_id, text=f'{client.name} {client.surname} принял твою заявку,'
                                                           f' теперь ты можешь просмотреть его в списке клиентов')
        await callback.message.delete()
        await callback.answer()
    elif callback_data.option == YesNoOptions.no:
        client = get_client_by_id(tg_id=callback.from_user.id)
        client_delete_trainer_request(client=client, trainer=trainer)
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"Заявка от ${trainer.name} ${trainer.surname} была удалена",
                               reply_markup=create_client_main_menu_keyboard(client=client))
        await bot.send_message(chat_id=trainer.tg_id, text=f'{client.name} {client.surname} отклонил твою заявку')
        await callback.message.delete()
        await callback.answer()







