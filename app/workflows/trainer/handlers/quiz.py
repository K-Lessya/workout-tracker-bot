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
from app.callbacks.callbacks import MoveCallback
from app.workflows.trainer.utils.keyboards.quiz import QuizKeyboard
from app.s3.downloader import create_presigned_url
from aiogram.types.menu_button_web_app import MenuButtonWebApp
from aiogram.types import WebAppInfo
from app.utilities.helpers_functions import callback_error_handler
from app.workflows.trainer.utils.keyboards.quiz import QuizKeyboard
from app.entities.single_file.crud import get_trainer


quiz_router = Router()

@quiz_router.callback_query(MoveCallback.filter(F.target == TrainerMainMenuMoveTo.quiz))
@callback_error_handler
async def show_quiz_keyboard(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    trainer = get_trainer(callback.from_user.id)
    lang = trainer.lang
    await bot.set_chat_menu_button(chat_id=callback.from_user.id,
                                   menu_button=MenuButtonWebApp(
                                       type="web_app",
                                       text='Cоздать Анкету',
                                       web_app=WebAppInfo(url="https://aryzhykau.github.io/workout-bot-webapp/")
                                   ))
    await callback.message.edit_text("Воспользуйся кнопкой меню", reply_markup=QuizKeyboard(lang).as_markup())
    await callback.answer()

