from aiogram.filters.callback_data import CallbackData


class ChooseCallback(CallbackData, prefix='choose'):
    target: str
    option: str


class MoveToCallback(CallbackData, prefix='move_to'):
    move_to: str


class YesNoOptions:
    yes = 'yes'
    no = 'no'


class TestCallback(CallbackData, prefix='test'):
    test_task: str
    user: str


class TestTasks:
    delete_me = 'delete_user'

