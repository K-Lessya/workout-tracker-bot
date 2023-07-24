from aiogram.fsm.state import StatesGroup, State


class AddClientStates(StatesGroup):
    process_username = State()
    process_contact = State()
    process_existing = State()


class AddExercisesSates(StatesGroup):
    process_body_part_name = State()
    process_muscle_group_name = State()
    process_exercise_name = State()
    process_photo = State()
    process_video = State()


class TrainerStates(StatesGroup):
    add_client = AddClientStates()
    add_exercise = AddExercisesSates()
