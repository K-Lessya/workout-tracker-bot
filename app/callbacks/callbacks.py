from aiogram.filters.callback_data import CallbackData


class ChooseCallback(CallbackData, prefix="choose"):
    target: str
    option: str


class MoveCallback(CallbackData, prefix="move"):
    target: str