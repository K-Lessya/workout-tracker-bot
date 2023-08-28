import traceback

from app.bot import bot
import re
import logging
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
                await state.update_data({'button_clicked': False})
        except Exception as e:
            paste = traceback.format_exc()

            error_message = f"An error occurred in function {func.__name__}: {str(traceback.format_exception_only(e))}"
            logging.log(level=logging.ERROR, msg=f"An error occurred in function {func.__name__}: {str(paste)}")


            await bot.send_message(callback.from_user.id, error_message)
    return wrapper

