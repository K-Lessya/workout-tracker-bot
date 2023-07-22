from aiogram.utils.keyboard import InlineKeyboardBuilder
from .buttons import MenuButton
from app.bot import bot


def create_keyboard(buttons: MenuButton):
    builder = InlineKeyboardBuilder()

    for single_button in buttons:
        builder.button(text=single_button.text, callback_data=single_button.callback_data)

    builder.adjust(1, 1)
    return builder.as_markup()


class Menu:
    def __init__(self, name, text, buttons):
        self.name = name
        self.text = text
        self.keyboard = create_keyboard(buttons=buttons)


    async def show_menu(self, chat_id, edit, message_id):
        if not edit:
            await bot.send_message(chat_id=chat_id, text=self.text, reply_markup=self.keyboard)
        else:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=self.text, reply_markup=self.keyboard)
