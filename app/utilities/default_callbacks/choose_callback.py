from aiogram.filters.callback_data import CallbackData


class ChooseCallback(CallbackData, prefix='choose'):
    target: str
    option: str


class YesNoOptions:
    yes = 'yes'
    no = 'no'
