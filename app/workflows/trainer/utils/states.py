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
    process_save = State()


class ListExercisesStates(StatesGroup):
    list_body_parts = State()
    list_muscle_groups = State()
    list_exercises = State()
    show_exercise = State()


class ExercisesDb(StatesGroup):
    add_exercise = AddExercisesSates
    list_exercises = ListExercisesStates


class TrainerStates(StatesGroup):
    add_client = AddClientStates()
    exercises_db = ExercisesDb()

