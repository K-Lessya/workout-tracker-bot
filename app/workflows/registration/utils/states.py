from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    ask_for_user_type = State()
    process_name = State()
    process_surname = State()
    process_visibility = State()
    process_photo = State()

