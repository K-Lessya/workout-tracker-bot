class TrainerMainMenuTargets:
    add_client = 'add_client'
    list_exercises = 'list_exercises'
    create_body_part = 'create_bodypart'
    create_muscle_group = 'create_mscl_grp'
    choose_existing_client = 'chhose_existing'
    show_clients = 'shw_clients'
    go_to_main_menu = 'to_trainer_main_menu'


class TrainerAddClientTargets:
    by_username = 'by_username'
    by_contact = 'by_contact'
    by_existing = 'by_existing'
    add_existing_client = 'add_existing'


class ListBodyPartsTargets:
    show_body_part = 'show_body_part'
    add_exercise = 'add_exercise'


class ListBodyPartsOptions:
    add_pure_exercise = 'add_pure_exercise'


class ListMuscleGroupsOptions:
    add_exercise_with_bodypart = 'add_exr_with_bodypart'


class CreateExerciseTargets:
    ask_for_exercise_photo = 'ask_for_exr_photo'
    process_exercise_photo = 'process_exercise_photo'
    process_exercise_video = 'process_exercise_video'
    process_save_exercise = 'process_save_exercise'