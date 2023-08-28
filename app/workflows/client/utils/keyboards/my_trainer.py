from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.workflows.client.utils.callback_properties.movetos import ClientMyTrainerMoveTo, ClientMainMenuMoveTo
from app.callbacks.callbacks import MoveCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo


class MyTrainerKeyboard(InlineKeyboardBuilder):
    def __init__(self):
        super().__init__()
        self.row(InlineKeyboardButton(text="Заполнить анкету",
                                      callback_data=MoveCallback(target=ClientMyTrainerMoveTo.fill_questionaire).pack()))
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=CommonGoBackMoveTo.to_client_main_menu).pack()))



class MyTrainerQuestionaireKeyboard(InlineKeyboardBuilder):
    def __init__(self):
        super().__init__()
        self.row(InlineKeyboardButton(text="Назад",
                                      callback_data=MoveCallback(target=ClientMainMenuMoveTo.my_trainer).pack()))
