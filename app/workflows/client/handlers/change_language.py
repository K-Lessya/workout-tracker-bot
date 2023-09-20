from aiogram import Router, F
from app.callbacks.callbacks import MoveCallback
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientChangeLanguageTarget
from app.utilities.helpers_functions import callback_error_handler
from app.entities.single_file.crud import get_client_by_id
from app.translations.base_translations import translations
from app.workflows.client.utils.keyboards.choose_language import ChooseLanguageKeyboard
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard



client_change_language_router = Router()


@client_change_language_router.callback_query(MoveCallback.filter(F.target == ClientMainMenuMoveTo.change_language))
@callback_error_handler
async def process_choose_language(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    client = get_client_by_id(callback.from_user.id)
    lang = client.lang
    await callback.message.edit_text(text=translations[lang].trainer_choose_language.value,
                                     reply_markup=ChooseLanguageKeyboard(lang).as_markup())

@client_change_language_router.callback_query(ChooseCallback.filter(F.target == ClientChangeLanguageTarget.choose_language))
@callback_error_handler
async def choose_language(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    new_lang = callback_data.option
    client = get_client_by_id(callback.from_user.id)
    client.lang = new_lang
    client.save()
    await callback.message.edit_text(text=translations[new_lang].registration_finish_trainer.value,
                                     reply_markup=create_client_main_menu_keyboard(client=client, lang=new_lang))


