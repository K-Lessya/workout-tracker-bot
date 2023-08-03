from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    process_user_name = State()
    process_user_surname = State()
    ask_for_user_photo = State()
    process_user_photo = State()
    ask_for_user_visibility = State()
    process_user_visibility = State()
    ask_for_user_save = State()
    process_user_save = State()
