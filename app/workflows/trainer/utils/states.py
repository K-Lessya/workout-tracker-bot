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
    ask_for_video = State()
    process_video = State()
    process_save = State()


class ListExercisesStates(StatesGroup):
    list_body_parts = State()
    list_muscle_groups = State()
    list_exercises = State()
    show_exercise = State()


class ExercisesDb(StatesGroup):
    process_buttons = State()
    add_exercise = AddExercisesSates
    list_exercises = ListExercisesStates


class ClientTraining(StatesGroup):
    process_comment = State()
    working_with_menu = State()


class CreatePlan(StatesGroup):
    process_day_name = State()
    process_num_days = State()
    process_body_parts = State()
    process_trainer_note = State()
    process_num_runs = State()
    process_num_repeats = State()

class MyClients(StatesGroup):
    create_plan = CreatePlan()
    client_training = ClientTraining()


class TrainerStates(StatesGroup):
    add_client = AddClientStates()
    exercises_db = ExercisesDb()
    my_clients = MyClients()





