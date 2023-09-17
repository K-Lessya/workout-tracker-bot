from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.callbacks.targets.registration import RegistrationTargets
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, YesNoOptions
from app.bot import bot
from app.callbacks.options.registration import RegistrationOptions
from app.states.registration.states import RegistrationStates
from app.keyboards.yes_no import YesNoKeyboard
from app.entities.single_file.crud import *
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions
from app.workflows.trainer.utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard
from app.s3.uploader import upload_file
from app.workflows.registration.utils.states import RegisterStates
from app.utilities.helpers_functions import album_handler
from app.translations.base_translations import translations
from app.keyboards.registration.keyboards import ChooseUsrTypeKeyboard

import os


registration_router = Router()

@registration_router.callback_query(ChooseCallback.filter(F.target == RegistrationTargets.choose_user_language))
async def set_user_language(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    lang = callback_data.option
    await state.update_data({'user_lang': lang})
    client = get_client_by_id(tg_id=callback.from_user.id)
    if client and not client.name:
        await state.set_state(RegistrationStates.process_user_name)
        await state.update_data({'usr_type': ChooseUsrTypeOptions.client, 'lang': lang})
        usr_type = RegistrationOptions.client
        msg_text = translations[client.lang].already_added_client_welcome_message_1 \
                             .value+client.trainer.name \
                             + client.trainer.surname \
                             + translations[client.lang].already_added_client_welcome_message_2.value
        await callback.message.edit_text(msg_text)
    else:
        await callback.message.edit_text(text=translations[lang].user_type_question.value,
                                         reply_markup=ChooseUsrTypeKeyboard(lang).as_markup())


@registration_router.callback_query(ChooseCallback.filter(F.target == RegistrationTargets.choose_user_type))
async def start_registration_process(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['user_lang']
    if 'process_user' in state_data:
        await callback.answer(text=translations[lang].finish_registration_alert.value, show_alert=True)
        await callback.message.delete()
    else:
        await state.update_data({'process_user': True})
        if callback_data.option == RegistrationOptions.trainer:
            if get_client_by_id(tg_id=callback.from_user.id):
                await callback.answer(text=translations[lang].registration_already_registered_client.value, show_alert=True)
                await callback.message.delete()
            elif get_trainer(tg_id=callback.from_user.id):
                await callback.answer(text=translations[lang].registration_already_registered_trainer.value, show_alert=True)
                await callback.message.delete()
            else:
                usr_type = RegistrationOptions.trainer
                msg_text = translations[lang].registration_ask_name_trainer.value

        elif callback_data.option == RegistrationOptions.client:
            if get_trainer(tg_id=callback.from_user.id):
                await callback.answer(text=translations[lang].registration_already_registered_trainer.value, show_alert=True)
                await callback.message.delete()
            elif get_client_by_id(tg_id=callback.from_user.id):
                await callback.answer(text=translations[lang].registration_already_registered_client.value, show_alert=True)
                await callback.message.delete()
            else:
                usr_type = RegistrationOptions.client
                msg_text = translations[lang].registration_ask_name_client.value

    await state.set_state(RegistrationStates.process_user_name)
    await state.update_data({"usr_type": usr_type})
    await callback.message.edit_text(msg_text)
    await callback.answer()


@registration_router.message(RegistrationStates.process_user_name)
async def process_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data['user_lang']
    await state.update_data({'name': message.text})
    await state.set_state(RegistrationStates.process_user_surname)
    await message.answer(translations[lang].registration_process_name.value.format(message.text))


@registration_router.message(RegistrationStates.process_user_surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data({'surname': message.text})
    state_data = await state.get_data()
    print(state_data)
    lang = state_data['user_lang']
    user_name = state_data['name']
    await state.set_state(RegistrationStates.ask_for_user_photo)

    await message.answer(translations[lang].registration_process_photo_question.value.format(user_name),
                         reply_markup=YesNoKeyboard(target=RegistrationTargets.process_user_photo, lang=lang).as_markup())


@registration_router.callback_query(ChooseCallback.filter(F.target == RegistrationTargets.process_user_photo))
async def declined_photo_message(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    usr_type = await state.get_data()
    lang = usr_type["user_lang"]
    if callback_data.option == YesNoOptions.no:
        await state.update_data({'photo_link': 'defaults/no-user-image-icon-0.png'})

        if usr_type['usr_type'] == RegistrationOptions.client:
            reply_str = translations[lang].registration_visibility_question_client.value

        elif usr_type['usr_type'] == RegistrationOptions.trainer:
            reply_str = translations[lang].registration_visibility_question_trainer.value

        await callback.message.edit_text(reply_str,
                                         reply_markup=YesNoKeyboard(target=RegistrationTargets.process_user_visibility,
                                                                    lang=lang).as_markup())
        await state.set_state(RegistrationStates.ask_for_user_visibility)
        await callback.answer()
    elif callback_data.option == YesNoOptions.yes:
        await state.update_data({'multiple_files_message_sent': False, 'file_recieved': False})
        await callback.message.edit_text(translations[lang].registration_process_photo.value)
        await state.set_state(RegistrationStates.process_user_photo)
        await callback.answer()


@registration_router.message(RegistrationStates.process_user_photo, F.photo)
@album_handler
async def process_photo(message: Message, state: FSMContext):
    destination = f'tmp/{message.photo[-1].file_id}.jpg'
    await bot.download(message.photo[-1], destination=destination)
    upload_file(file=destination, destination=f'users/{message.from_user.id}/avatar.jpg')
    os.remove(destination)
    await state.update_data({"photo_link": f"users/{message.from_user.id}/avatar.jpg"})
    await state.set_state(RegisterStates.process_visibility)

    user_type = await state.get_data()
    lang = user_type["user_lang"]

    if user_type['usr_type'] == RegistrationOptions.client:
        reply_str = translations[lang].registration_visibility_question_client.value

    elif user_type['usr_type'] == RegistrationOptions.trainer:
        reply_str = translations[lang].registration_visibility_question_trainer.value
    await state.set_state(RegistrationStates.ask_for_user_visibility)
    await message.answer(reply_str,
                         reply_markup=YesNoKeyboard(target=RegistrationTargets.process_user_visibility, lang=lang).as_markup())


@registration_router.message(RegistrationStates.process_user_photo, F.text)
async def process_photo(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data["user_lang"]
    await message.answer(translations[lang].registration_alert_waiting_for_photo.value)


@registration_router.callback_query(ChooseCallback.filter(F.target == RegistrationTargets.process_user_visibility))
async def process_visibility(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    await state.set_state(RegistrationStates.process_user_visibility)
    if callback_data.option == YesNoOptions.yes:
        visibility = True

    elif callback_data.option == YesNoOptions.no:
        visibility = False

    await state.update_data({'visibility': visibility})

    await state.set_state(RegistrationStates.process_user_save)
    user_info = await state.get_data()
    lang = user_info["user_lang"]
    if callback.from_user.username:
        username = callback.from_user.username
    else:
        username = None

    if user_info['usr_type'] == RegistrationOptions.client:
        if get_client_by_id(tg_id=callback.from_user.id):
            new_client = get_client_by_id(tg_id=callback.from_user.id)
            new_client.name = user_info['name']
            new_client.surname = user_info['surname']
            new_client.tg_username = username
            new_client.photo_link = user_info['photo_link']
            new_client.visibility = user_info['visibility']
            new_client.save()
        else:
            new_client = Client(tg_id=callback.from_user.id,
                                 name=user_info['name'],
                                 surname=user_info['surname'],
                                 tg_username=username,
                                 photo_link=user_info['photo_link'],
                                 visibility=user_info['visibility'],
                                 lang=user_info['user_lang']
                                )
            create_client(new_client)

        await callback.message.edit_text(
            translations[lang].registration_finish_client.value,
            reply_markup=create_client_main_menu_keyboard(client=new_client, lang=lang))

    elif user_info['usr_type'] == RegistrationOptions.trainer:
        create_trainer(Trainer(tg_id=callback.from_user.id,
                               name=user_info['name'],
                               tg_username=username,
                               surname=user_info['surname'],
                               photo_link=user_info['photo_link'],
                               visibility=user_info['visibility'],
                               lang=user_info['user_lang']))
        await callback.message.edit_text(translations[lang].registration_finish_trainer.value,
                                         reply_markup=create_trainer_main_menu_keyboard(lang=lang))

    await state.clear()
    await callback.answer()
