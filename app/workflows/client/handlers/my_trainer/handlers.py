from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery, MenuButtonWebApp, WebAppInfo, MenuButtonCommands
from app.bot import bot
from app.s3.downloader import create_presigned_url
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo, ClientMyTrainerMoveTo
from app.callbacks.callbacks import MoveCallback
from app.entities.single_file.models import Client, Trainer
from app.entities.single_file.crud import get_client_by_id, get_trainer
from app.config import PHOTO_BUCKET
from app.workflows.client.utils.keyboards.my_trainer import MyTrainerKeyboard, MyTrainerQuestionaireKeyboard
from app.translations.base_translations import translations

client_my_trainer_router = Router()


@client_my_trainer_router.callback_query(MoveCallback.filter(F.target == ClientMainMenuMoveTo.my_trainer))
async def show_my_trainer(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    client_id = callback.from_user.id
    client = get_client_by_id(tg_id=client_id)
    lang = client.lang
    if client.trainer:
        trainer = client.trainer
        msg_str = translations[lang].client_my_trainer.value.format(trainer.name, trainer.surname)
        if callback.message.photo:
            await bot.set_chat_menu_button(chat_id=callback.from_user.id, menu_button=MenuButtonCommands(type="commands"))
            await callback.message.edit_caption(caption=msg_str, reply_markup=MyTrainerKeyboard().as_markup())
        else:
            await callback.message.delete()
            trainer_photo = create_presigned_url(PHOTO_BUCKET, trainer.photo_link)
            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=trainer_photo,
                                 caption=msg_str,
                                 reply_markup=MyTrainerKeyboard(lang).as_markup())
    else:
        await callback.answer(text=translations[lang].client_my_trainer_no_trainer.value, show_alert=True)

@client_my_trainer_router.callback_query(MoveCallback.filter(F.target == ClientMyTrainerMoveTo.fill_questionaire))
async def fill_questionare(callback: CallbackQuery, callback_data: MoveCallback, state: FSMContext):
    await bot.set_chat_menu_button(chat_id=callback.from_user.id,
                                   menu_button=MenuButtonWebApp(
                                       type="web_app",
                                       text='Cоздать Анкету',
                                       web_app=WebAppInfo(url="https://aryzhykau.github.io/workout-bot-webapp/")))
    await callback.message.edit_caption(caption="Воспользуйся кнопкой внизу", reply_markup=MyTrainerQuestionaireKeyboard().as_markup())
    await callback.answer("Загрузка завершена")


