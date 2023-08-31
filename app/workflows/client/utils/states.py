from aiogram.fsm.state import StatesGroup, State


class ShowClientPlan(StatesGroup):
    show_days = State()
    show_exercises = State()
    show_single_exercise = State()


class AddTrainingFromPlan(StatesGroup):
    show_plan = State()
    show_day = State()
    show_exercise = State()
    process_exercise_weight = State()
    process_exercise_video = State()
    ask_for_client_note = State()
    process_client_note = State()


class AddCustomTraining(StatesGroup):
    process_training_name = State()
    process_buttons = State()
    process_exercise_name = State()
    process_exercise_repeats = State()
    process_exercise_runs = State()
    process_exercise_weight = State()
    process_exercise_video = State()


class AddTraining(StatesGroup):
    process_training_type = State()
    add_from_plan = AddTrainingFromPlan()
    add_custom = AddCustomTraining()


class ClientStates(StatesGroup):
    start_state = State()
    add_training = AddTraining()
    show_client_plan = ShowClientPlan()



