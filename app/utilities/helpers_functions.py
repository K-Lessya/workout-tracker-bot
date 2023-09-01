import traceback

from app.bot import bot
from aiogram.types import Message
import re
import logging
from app.config import MAX_FILE_SIZE
from aiogram.types import CallbackQuery


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def process_tg_link(link: str):
    if "https://t.me/" in link:
        return link.replace("https://t.me/", "")
    else:
        return link


def check_link(link: str):
    if re.match("https://t.me", link) or re.match("http://t.me", link):
        return True
    else:
        return False

def double_button_click_handler(func):
    async def wrapper(callback, callback_data, state):
        data = await state.get_data()
        if data.get('button_clicked'):
            if data['button_clicked']:
                await callback.answer(text="Ты уже нажал кнопку, подожди загрузки", show_alert=True)
            else:
                await func(callback, callback_data, state)
        else:
            await func(callback, callback_data, state)
        return wrapper

def callback_error_handler(func):

    async def wrapper(callback, callback_data, state):
        try:
            data = await state.get_data()
            if data.get('button_clicked'):
                if data['button_clicked']:
                    await callback.answer('Дождись загрузки', show_alert=True)
                else:
                    await state.update_data({'button_clicked': True})
                    logging.log(level=logging.INFO, msg=f"Executing {func.__name__}")
                    await func(callback, callback_data, state)
                    await state.update_data({'button_clicked': False})
            else:
                await state.update_data({'button_clicked': True})
                logging.log(level=logging.INFO, msg=f"Executing {func.__name__}")
                await func(callback, callback_data, state)

        except Exception as e:
            paste = traceback.format_exc()

            error_message = f"An error occurred in function {func.__name__}: {str(traceback.format_exception_only(e))}"
            logging.log(level=logging.ERROR, msg=f"An error occurred in function {func.__name__}: {str(paste)}")
            await bot.send_message(callback.from_user.id, error_message)
        finally:
            await state.update_data({'button_clicked': False})



    return wrapper



async def process_message_video(message: Message):
    if message.video.file_size < MAX_FILE_SIZE:
        file = await bot.get_file(message.video.file_id)
        file_path = file.file_path
        file_destination = file_path.replace("/", "_")
        await bot.download_file(file_path=file_path, destination=file_destination)
        return file_destination
    else:
        await message.answer(f"Размер файла превышает максимально допустимый ({MAX_FILE_SIZE/1000000}MБ)")






