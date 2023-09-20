import os
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram import F
from app.bot import bot
from app.keyboards.yes_no import YesNoKeyboard
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
from app.translations.base_translations import translations

client_request_router = Router()

@client_request_router.callback_query(MoveCallback.filter(F.target == ClientMainMenuMoveTo.my_recieved_requests))
@callback_error_handler
async def show_requests(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
    await state.clear()
    client = get_client_by_id(callback.from_user.id)
    lang = client.lang
    await state.update_data({'lang': lang})
    client_requests = get_client_requests_by_id(tg_id=callback.from_user.id)
    await callback.message.edit_text(translations[lang].client_requests_menu.value,
                                     reply_markup=create_client_income_requests_keyboard(options=client_requests,
                                         target=ClientIncomeRequestTargets.show_income_request,
                                         go_back_filter=MoveCallback(target=CommonGoBackMoveTo.to_client_main_menu),
                                         lang=lang))
@client_request_router.callback_query(ChooseCallback.filter(F.target == ClientIncomeRequestTargets.show_income_request))
@callback_error_handler
async def show_income_request(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await callback.message.delete()
    state_data = await state.get_data()
    lang = state_data['lang']
    trainer = get_trainer_by_obj_id(obj_id=callback_data.option)
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET,object_name=trainer.photo_link)
    await state.update_data({'trainer': trainer})
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                         caption=translations[lang].client_requests_show_request.value.format(trainer.name, trainer.surname),
                         reply_markup=YesNoKeyboard(target=ClientIncomeRequestTargets.process_income_request, lang=lang).as_markup())

@client_request_router.callback_query(ChooseCallback.filter(F.target == ClientIncomeRequestTargets.process_income_request))
@callback_error_handler
async def process_income_request(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    trainer = state_data['trainer']
    if callback_data.option == YesNoOptions.yes:
        await callback.message.delete()
        client = get_client_by_id(tg_id=callback.from_user.id)
        update_client_trainer(client=client, trainer=trainer)
        client_delete_trainer_request(client=client, trainer=trainer)
        await bot.send_message(chat_id=callback.from_user.id,
                               text=translations[lang].client_requests_accept_request.value.format(trainer.name,
                                                                                                   trainer.surname),
                               reply_markup=create_client_main_menu_keyboard(client=client, lang=lang))

        await bot.send_message(chat_id=trainer.tg_id,
                               text=translations[trainer.lang].client_requests_accept_request_trainer_notification
                               .value.format(client.name, client.surname))


        await callback.answer()
    elif callback_data.option == YesNoOptions.no:
        await callback.message.delete()
        client = get_client_by_id(tg_id=callback.from_user.id)
        client_delete_trainer_request(client=client, trainer=trainer)
        await bot.send_message(chat_id=callback.from_user.id,
                               text=translations[lang].client_requests_decline_request.value.format(trainer.name,
                                                                                                    trainer.surname),
                               reply_markup=create_client_main_menu_keyboard(client=client, lang=lang))
        await bot.send_message(chat_id=trainer.tg_id, text=translations[trainer.lang]
                               .client_requests_decline_request_trainer_notification.value.format(client.name,
                                                                                                  client.surname))

        await callback.answer()







