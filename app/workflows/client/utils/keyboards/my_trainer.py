from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.workflows.client.utils.callback_properties.movetos import ClientMyTrainerMoveTo, ClientMainMenuMoveTo
from app.callbacks.callbacks import MoveCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.translations.base_translations import translations


class MyTrainerKeyboard(InlineKeyboardBuilder):
    def __init__(self, lang):
        super().__init__()
        self.row(InlineKeyboardButton(text=translations[lang].client_fill_questionnaire.value,
                                      callback_data=MoveCallback(target="to_no_content").pack()))
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=MoveCallback(target=CommonGoBackMoveTo.to_client_main_menu).pack()))



class MyTrainerQuestionaireKeyboard(InlineKeyboardBuilder):
    def __init__(self, lang):
        super().__init__()
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=MoveCallback(target=ClientMainMenuMoveTo.my_trainer).pack()))
