from aiogram import Router, F
from app.callbacks.callbacks import MoveCallback
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from app.workflows.trainer.utils.callback_properties.movetos import TrainerMainMenuMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMainMenuTargets
from app.utilities.helpers_functions import callback_error_handler
from app.entities.single_file.crud import get_trainer
from app.translations.base_translations import translations
from app.workflows.trainer.utils.keyboards.choose_language import ChooseLanguageKeyboard
from app.workflows.trainer.utils.keyboards.trainer_main_menu import create_trainer_main_menu_keyboard



trainer_change_language_router = Router()


@trainer_change_language_router.callback_query(MoveToCallback.filter(F.move_to == TrainerMainMenuMoveTo.change_language))
@callback_error_handler
async def process_choose_language(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    await callback.message.edit_text(text=translations[lang].trainer_choose_language.value,
                                     reply_markup=ChooseLanguageKeyboard(lang).as_markup())

@trainer_change_language_router.callback_query(ChooseCallback.filter(F.target == TrainerMainMenuTargets.choose_language))
@callback_error_handler
async def choose_language(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    new_lang = callback_data.option
    trainer = get_trainer(callback.from_user.id)
    trainer.lang = new_lang
    trainer.save()
    await callback.message.edit_text(text=translations[new_lang].registration_finish_trainer.value,
                                     reply_markup=create_trainer_main_menu_keyboard(new_lang))


