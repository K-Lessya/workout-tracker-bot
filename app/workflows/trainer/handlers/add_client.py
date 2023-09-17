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
from app.translations.base_translations import translations

add_client_router = Router()

@add_client_router.callback_query(MoveToCallback.filter(F.move_to == TrainerMainMenuMoveTo.add_client))
@callback_error_handler
async def choose_add_flow(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    lang = get_trainer(callback.from_user.id).lang
    await callback.message.edit_text(translations[lang].trainer_add_client_menu_choose_add_method.value,
                                     reply_markup=create_add_client_options_keyboard(lang=lang))
    await callback.answer()


@add_client_router.callback_query(MoveToCallback.filter(F.move_to == AddClientMoveTo.by_contact))
@callback_error_handler
async def start_add_client(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    lang = get_trainer(callback.from_user.id).lang
    await state.set_state(TrainerStates.add_client.process_contact)
    await callback.message.edit_text(translations[lang].trainer_add_client_menu_share_contact.value)
    await callback.answer()


@add_client_router.message(TrainerStates.add_client.process_contact)
async def process_client_contact(message: Message, state: FSMContext):
    lang = get_trainer(message.from_user.id).lang
    if get_trainer(message.contact.user_id):
        await message.answer(translations[lang].trainer_add_client_menu_already_registered_as_trainer.value,
                             reply_markup=create_trainer_main_menu_keyboard(lang=lang))
        await state.clear()
    else:
        if get_client_by_id(message.contact.user_id):
            client = get_client_by_id(message.contact.user_id)
            if client.trainer:
                if client.trainer.tg_id == message.from_user.id:
                    await message.answer(translations[lang].trainer_add_client_menu_client_already_added.value,
                                         reply_markup=create_trainer_main_menu_keyboard(lang=lang))
                else:
                    await message.answer(translations[lang].trainer_add_client_menu_client_already_has_another_trainer.value,
                                         reply_markup=create_trainer_main_menu_keyboard(lang))
            else:
                trainer = get_trainer(tg_id=message.from_user.id)
                update_client_trainer(client=client, trainer=trainer)
        else:
            create_client(Client(tg_id=message.contact.user_id, phone_number=message.contact.phone_number,
                                 trainer=get_trainer(message.from_user.id)))
            await state.clear()
            await message.answer(translations[lang].trainer_add_client_menu_client_added_successfully.value,
                                 reply_markup=create_trainer_main_menu_keyboard(lang))

@add_client_router.callback_query(MoveToCallback.filter(F.move_to == AddClientMoveTo.by_existing))
@callback_error_handler
async def add_client_by_existing(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    clients = get_all_not_assigned_clients_with_name()
    lang = get_trainer(callback.from_user.id).lang
    print(clients)
    if clients:
        await callback.message.edit_text(translations[lang].trainer_add_client_menu_select_from_list.value,
                                         reply_markup=create_choose_existing_clients_keyboard(clients=clients,
                                                                                              lang=lang))
    else:
        await callback.answer(translations[lang].trainer_add_client_menu_all_clients_already_have_trainer.value,
                              show_alert=True)

    await callback.answer()


@add_client_router.callback_query(ChooseCallback.filter(F.target == TrainerAddClientTargets.show_clients))
@callback_error_handler
async def show_user_profile(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    client = get_client_by_id(int(callback_data.option))
    lang = get_trainer(callback.from_user.id).lang
    photo_link = create_presigned_url(bucket_name=PHOTO_BUCKET, object_name=client.photo_link)
    await state.update_data({'tg_id': client.tg_id})
    await bot.send_photo(chat_id=callback.from_user.id, photo=photo_link,
                         caption=translations[lang].trainer_add_client_menu_add_client_profile.value
                         .value.format({client.name}, {client.surname}),
                         reply_markup=create_yes_no_keyboard(target=TrainerAddClientTargets.add_existing_client))
    await callback.message.delete()
    await callback.answer()


@add_client_router.callback_query(ChooseCallback.filter(F.target == TrainerAddClientTargets.add_existing_client))
@callback_error_handler
async def add_client_profile(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    if callback_data.option == YesNoOptions.yes:
        state_data = await state.get_data()
        client_id = state_data['tg_id']
        client = get_client_by_id(client_id)
        trainer = get_trainer(callback.from_user.id)
        lang = trainer.lang
        client_add_new_trainer_request(client, trainer)
        await state.clear()
        await bot.send_message(chat_id=callback.from_user.id,
                               text=translations[lang].trainer_add_client_menu_request_sent.value,
                               reply_markup=create_trainer_main_menu_keyboard(lang=lang))
        await bot.send_message(chat_id=client_id, text=translations[client.lang].trainer_add_client_menu_request_text.value,
                               reply_markup=create_new_trainer_request_keyboard(str(trainer.id)))
        await callback.message.delete()
    elif callback_data.option == YesNoOptions.no:
        clients = get_all_not_assigned_clients_with_name()
        lang = get_trainer(callback.from_user.id).lang
        await state.clear()
        await bot.send_message(chat_id=callback.from_user.id,
                               text=translations[lang].trainer_add_client_menu_watch_others.value,
                               reply_markup=create_choose_existing_clients_keyboard(clients))
        await callback.message.delete()
    await callback.answer()

@add_client_router.callback_query(MoveToCallback.filter(F.move_to == CommonGoBackMoveTo.to_trainer_main_menu))
@callback_error_handler
async def go_to_main_menu(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    lang = get_trainer(callback.from_user.id).lang
    await callback.message.edit_text(translations[lang].trainer_add_client_menu_back_to_main_menu.value,
                                     reply_markup=create_trainer_main_menu_keyboard(lang=lang))
    await bot.set_chat_menu_button(chat_id=callback.from_user.id, menu_button=MenuButtonCommands(type='commands'))
    await callback.answer()

