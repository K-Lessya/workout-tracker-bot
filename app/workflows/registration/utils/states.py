from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    process_name = State()
    process_surname = State()
    process_visibility = State()
    process_photo = State()

