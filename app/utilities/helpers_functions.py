import traceback

from app.bot import bot
from aiogram.types import Message
import re
import logging
from app.config import MAX_FILE_SIZE
from app.translations.base_translations import translations
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


def album_handler(func):
    async def wrapper(message, state):
        state_data = await state.get_data()
        lang = state_data['lang']
        print(state_data['multiple_files_message_sent'])
        if not state_data['multiple_files_message_sent']:
            print("message was not send yet, sending ...")
            if not state_data['file_recieved']:
                print(f'handled file from message {message.message_id}')
                await state.update_data({'file_recieved': True})
                await func(message, state)
            else:
                print(f'another file catched sending message')
                await state.update_data({"multiple_files_message_sent": True})
                print('STATE UPDATED')
                await message.answer(translations[lang].multiple_files_alert.value)

        else:
            print('another file catched but message was already sent')
    return wrapper




def callback_error_handler(func):

    async def wrapper(callback, callback_data, state):
        try:
            GREEN = "\033[92m"
            RESET = "\033[0m"
            data = await state.get_data()
            state_name = await state.get_state()
            if data.get('button_clicked'):
                if data['button_clicked']:
                    await callback.answer('Дождись загрузки', show_alert=True)
                else:
                    await state.update_data({'button_clicked': True})

                    logging.log(level=logging.INFO, msg=f"Executing {func.__name__}")
                    logging.log(level=logging.INFO, msg=f"{GREEN}state before function {state_name}{RESET} ")
                    await func(callback, callback_data, state)
                    state_name = await state.get_state()
                    logging.log(level=logging.INFO, msg=f"{GREEN}state after function {state_name}{RESET} ")
                    await state.update_data({'button_clicked': False})
            else:
                await state.update_data({'button_clicked': True})
                logging.log(level=logging.INFO, msg=f"Executing {func.__name__}")
                logging.log(level=logging.INFO, msg=f"{GREEN}state before function {state_name}{RESET} ")
                await func(callback, callback_data, state)
                state_name = await state.get_state()
                logging.log(level=logging.INFO, msg=f"{GREEN}state after function {state_name}{RESET} ")

        except Exception as e:
            paste = traceback.format_exc()

            error_message = f"An error occurred in function {func.__name__}: {str(traceback.format_exception_only(e))}"
            logging.log(level=logging.ERROR, msg=f"An error occurred in function {func.__name__}: {str(paste)}")
            await bot.send_message(callback.from_user.id, error_message)
        finally:
            await state.update_data({'button_clicked': False})



    return wrapper



async def process_message_video(message: Message, file_name):
    if message.video.file_size < MAX_FILE_SIZE:
        file = await bot.get_file(message.video.file_id)
        file_path = file.file_path
        file_destination = f'tmp/{file_name}.{file_path.split(".")[1]}'
        await bot.download_file(file_path=file_path, destination=file_destination)
        return file_destination
    else:
        await message.answer(f"Размер файла превышает максимально допустимый ({MAX_FILE_SIZE/1000000}MБ)")






