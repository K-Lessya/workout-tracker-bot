from aiogram.fsm.state import StatesGroup, State


class ClientStates(StatesGroup):
    start_state = State()
    process_training_name = State()
    process_exercise_name = State()
    process_exercise_repeats = State()
    process_exercise_runs = State()
    process_exercise_weight = State()
    process_exercise_video = State()

