from enum import Enum


class EnglishTranslations(Enum):
    user_type_question = 'Hi, do you want to register as client or as trainer?'
    main_menu_text = 'Hi again! Choose one of the menu options'
    already_added_client_welcome_message_1 = "Hi, you've been added to this bot by trainer "
    already_added_client_welcome_message_2 = ", let's continue your registration process\nEnter your name pls"
    finish_registration_alert = 'You need to end current registration process'
    registration_ask_name_trainer = "Hi new trainer, what is your name?"
    registration_ask_name_client = "Hi new client, what is your name?"
    registration_already_registered_trainer = "You are already registered as a trainer"
    registration_already_registered_client = "You are already registered as a client"
    registration_process_name = "Great {}, now tell me your surname"
    registration_process_photo_question = "Super {}, do you want to upload a photo?"
    registration_process_photo = "Then send me your best photo!"
    registration_alert_waiting_for_photo = "I'm waiting for photo"
    registration_visibility_question_trainer = "Nice, do you want to make your profile visible for clients"
    registration_visibility_question_client = "Nice, do you want to make your profile visible for trainers"
    registration_finish_client = 'Welcome to the client menu, here you can add your trainings and' \
                                 ' see information about already added trainings'
    registration_finish_trainer = 'Welcome to the trainer menu, here you can add clients, create training plan for' \
                                  ' each of your clients and watch their trainings'

    use_btn_alert = "Use one of the buttons pls"
    usr_type_btn_client = "Client"
    usr_type_btn_trainer = "Trainer"
    yes_no_btn_yes = "Yes"
    yes_no_btn_no = "No"

    client_menu_btn_add_training = "Add training"
    client_main_menu_btn_my_requests = "My requests({})"
    client_main_menu_btn_my_trainings = "My trainings"
    client_main_menu_btn_my_trainer = "My trainer"
    client_main_menu_btn_my_plan = "My plan"

    trainer_choose_language = "Сhoose language"

    trainer_add_client_menu_choose_add_method = "Select the adding method please"
    trainer_add_client_menu_share_contact = "Then share a client contact with me and i will add him(her)," \
                                            " you will see him in your clients list after he(she) will finish" \
                                            " registration process"
    trainer_add_client_menu_already_registered_as_trainer = "This profile is registered as a trainer, you can't" \
                                                            " add it"
    trainer_add_client_menu_client_already_added = "You already have this client in your list"
    trainer_add_client_menu_client_already_has_another_trainer = "This client already has a trainer, you can't " \
                                                                 "add him(her)"
    trainer_add_client_menu_client_added_successfully = "Client added successfully"
    trainer_add_client_menu_select_from_list = "Select client from the list"
    trainer_add_client_menu_all_clients_already_have_trainer = "All clients already have a trainer"
    trainer_add_client_menu_add_client_profile = "Name: {}\nSurname: {}\nDo you want to add this client?"
    trainer_add_client_menu_request_sent = "Request was sent to client"
    trainer_add_client_menu_request_text = "You have new request from trainer, take a look"
    trainer_add_client_menu_watch_others = "Well, let's see other clients"
    trainer_add_client_menu_back_to_main_menu = "We are in main menu again"

    trainer_add_exercise_choose_body_part = 'Type the exercise body part name or select one from the list'
    trainer_add_exercise_create_muscle_group_message = 'Type the exercise muscle group name'
    trainer_add_exercise_create_muscle_group_callback = 'Type the exercise muscle group name or select it from the list'
    trainer_add_exercise_type_exercise_name = "Now type the exercise name"
    trainer_add_exercise_ask_for_media = "Do you want to upload photo or video that will show exercise technique?"
    trainer_add_exercise_process_media = 'Then send me the photo or the video that will show exercise technique\n' \
                                         'It will be better if photo will consist of two positions in exercise'
    trainer_add_exercise_process_media_text_recieved = "You need to send photo or video"
    trainer_add_exercise_process_media_file_size_alert = "File size must be less, than 50Мб"
    trainer_add_exercise_ask_for_save = 'Check your exercise.\nBody part: {}\nMuscle group:' \
                                        ' {}\nExercise name: {}\n Do you want to save it?'
    trainer_add_exercise_process_save_loading = "Saving exercise..."
    trainer_add_exercise_process_save_process_file = "Processing exercise media..."
    trainer_add_exercise_process_save_upload_file = "Uploading exercise file..."
    trainer_add_exercise_process_save_file_uploaded = "File uploaded"
    trainer_add_exercise_process_save_process_bp_mg = "Processing body part and muscle group..."
    trainer_add_exercise_process_save_not_saved = "Exercise was not saved"

    trainer_exercise_db_choose_bodypart = "Choose exercise by body part and muscle group"
    trainer_exercise_db_menu_choose_body_part = "Choose exercise's body part\n" \
                                                " If no body parts listed, create new exercise"
    trainer_exercise_db_menu_choose_muscle_group = "Choose muscle group"
    trainer_exercise_db_menu_choose_exercise = "Choose exercise"
    trainer_exercise_db_menu_sending_exercie_media = "Sending exercise media"
    trainer_exercise_db_menu_inline_create_body_part = "This message will start exercise creation process(will be handled as body part name)\n" \
                                                       "Body part {} " \
                                                       "Now type muscle group name"
    trainer_exercise_db_menu_inline_create_muscle_group = "This message will start exercise creation process(will be handled as muscle group name)\n" \
                                                          "Body part {}\n" \
                                                          "Muscle group {}\n" \
                                                          "Now enter the exercise name"
    trainer_exercise_db_menu_inline_create_exercise = "This message will start exercise creation process(will be handled as exercise name)" \
                                                      "Do you want to upload exercise's technique photo or video?"

    trainer_my_clients_menu_my_clients = "My clients menu\nSelect from the list"
    trainer_my_clients_menu_no_clients_registered = "No one from your selected clients completed registration or accepted your request"
    trainer_my_clients_menu_no_clients = "You don't have any clients now\nAdd them from add client menu"
    trainer_my_clients_menu_single_client_menu = "Client:\nName: {}\nSurname: {}"
    trainer_my_clients_menu_single_client_create_plan_select_exercise = "Let's choose exercise for day {}, or you can create new exercise"

    trainer_my_clients_menu_single_client_create_plan_start = "Creating plan for client {} {}.\n" \
                                                              "Add new day or edit existing one"
    trainer_my_clients_menu_single_client_create_plan_day_name = "Type the name of the day {}"
    trainer_my_clients_menu_single_client_create_plan_no_exercises = "There are no exercise in your db yet, just add one"
    trainer_my_clients_menu_single_client_create_plan_add_trainer_note = "Add your own recommendation(hint) about the" \
                                                                         " base technique(It's a basic " \
                                                                         "recommendation, which will be shown " \
                                                                         "with exercise)\n Or if you don't want to add anything press" \
                                                                         " next"
    trainer_my_clietns_menu_single_client_create_plan_exercise_already_added = "You have already added this exercise into plan, please selec another exercise or save day"
    trainer_my_clietns_menu_single_client_create_plan_add_num_runs = "Type how many runs should be in exercise"
    trainer_my_clietns_menu_single_client_create_plan_add_num_repeats = "Type how many repeats should be in each run"
    trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added = "Trainer didn't add any hints"


    trainer_create_plan_choose_exercise_for_day = "Let's choose exercises for day {}"
    trainer_create_plan_add_trainer_note = 'Add your own note or recommendation for client about technique (This is a basic recommendation, which will be shown to client with an exercise)'
    trainer_my_clietns_menu_single_client_create_plan_add_one_more_or_save_day = "Add another exercise to this day or save it"
    trainer_my_clients_menu_single_clietn_create_plan_save_client_notification = "{} {} just created a training plan for you"
    trainer_my_clients_menu_single_clietn_create_plan_save_trainer_alert = "Training plan was saved successfully, client can check it in menu"
    trainer_my_clients_menu_single_clietn_create_plan_save_plan_question = "Do you want to save plan?"

    trainer_my_clients_menu_single_client_plan_menu = "You can view current plan or create a new one"
    trainer_my_clients_menu_single_client_vieew_plan_show_days = "Choose a day from plan"
    trainer_my_clients_menu_single_client_vieew_plan_show_exercises = "Choose exercise"
    trainer_my_clients_menu_single_client_view_plan_load_data = "Loading data..."
    trainer_my_clients_menu_single_client_view_plan_send_photo = "Sending photo..."
    trainer_my_clients_menu_single_client_view_plan_get_video = "Getting video..."
    trainer_my_clients_menu_single_client_view_plan_send_video = "Sending video..."

    trainer_my_clients_menu_single_client_view_trainings_no_trainings = "Client has not added any training yet"
    trainer_my_clients_menu_single_client_view_trainings_choose_day = "Select training from the list"
    trainer_my_clients_menu_single_client_view_trainings_show_training = "Training {}\nDate: {}\nExercises:"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise = "Exercise: {}\n" \
                                                                         "Runs x Repeats: {}x{}\n" \
                                                                         "Working weight: {} kg"
    trainer_my_clients_menu_single_client_view_trainings_update_comment = "Update comment"
    trainer_my_clients_menu_single_client_view_trainings_create_comment = "Add comment"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_video = "Client note: {}\nTrainer comment: {}"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_video_no_comment = "Client note: {}\nNo trainer comment"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_as_for_comment = "Type your comment about client video"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_comment_saved = "Comment has been saved"

    trainer_main_menu_btn_add_client = "Add client"
    trainer_main_menu_btn_my_clients = "My clients"
    trainer_main_menu_btn_exercise_db = "Exercises database"
    trainer_main_menu_btn_questionaire = "Questionnaire for clients"
    trainer_main_menu_btn_change_language = "Change Language"
    trainer_add_client_btn_share_contact = "Share contact"
    trainer_add_client_btn_select_existed = "Add from already registered clients"

    trainer_my_clients_single_clietn_menu_btn_questionnaire = "Questionnaire"
    trainer_my_clients_single_clietn_menu_btn_trainings = "Trainings"
    trainer_my_clients_single_clietn_menu_btn_create_plan = "Create training plan"
    trainer_my_clients_single_clietn_menu_btn_show_plan = "Training plans"

    trainer_exercise_plan_list_keyboard_save_day = "Go back to other plan days"
    trainer_exercise_plan_list_keyboard_add_exercise = "Add exercise to day"

    trainer_my_clients_single_client_create_plan_menu = "Add day to plan"

    trainer_client_plan_menu_keyboard_show_plan = "Show client plan"
    trainer_client_plan_menu_keyboard_create_new_plan = "Create new plan"

    trainer_client_training_exercise_show_video_with_comments = "Show client video and comments"

    trainer_client_plan_days_keyboard_day_btn = "Day {}({})"

    trainer_add_exercise_btn_add_exercise = "Create exercise"
    trainer_create_plan_notification = "All changes that you will make will be saved automatically\nYou will be able to edit or add smomething later if you will decide to quit current plan creation process"
    ################## Client ########################
    client_main_menu = "ClientMenu"

    client_my_trainer = "Name: {}\nSurname: {}"
    client_my_trainer_no_trainer = "You don't have trainer yet"

    client_requests_menu = "Incoming requests from trainers"
    client_requests_show_request = "Request from trainer:\n{} {}\nAccept request?"
    client_requests_accept_request = "Congratulations, from now {} {} is your trainer"
    client_requests_accept_request_trainer_notification = "{} {} has accepted you request, now you can view him(her) in the clients list"
    client_requests_decline_request = "Request from {} {} was deleted"
    client_requests_decline_request_trainer_notification = "{} {} declined your request"

    client_my_plan_loading_data = "Loading data..."
    client_my_plan_choose_day = "Choose day"
    client_my_plan_show_day = "Here are your exercises for day {}, if you are struggling with technique just select exercise"
    client_my_plan_loading_video = "Loading media..."
    client_my_plan_show_exercise = "{}\n{} runs {} repeats\nTrainer note for you: {}"

    client_my_trainings_choose_training = "Choose training day"
    client_my_trainings_show_training = "Training {}\nDate: {}\nExercises:"
    client_my_trainings_show_exercise = "Exercise: {}\nAmount: {}x{}\nWorking weight: {} kg"
    client_my_trainings_show_video_client_comment = "My question: {}"
    client_my_trainings_show_video_no_client_comment = "You haven't left any questions\n"
    client_my_trainings_show_video_trainer_comment = "Trainer's comment: {}"
    client_my_trainings_show_video_no_trainer_comment = "Trainer still didn't added any comments about your technique"

    client_add_training_choose_training = "Do you want to add a custom training or add a traiing from your plan?"
    client_add_training_add_custom_start = "  You create your own exercises for custom trainings and in this trainings you are not allowed to:\n\n" \
                                           "- Use trainer's exercises\n" \
                                           "- See exercises techinque description and media\n" \
                                           "- Your trainer's personal recommendation about exercise technique\n" \
                                           "  All above is allowed only if you will create training from plan\n\n" \
                                           "  However you are still able to record your own videos of exercises and your trainer will be able to make corrections\n\n" \
                                           "  If you don't have trainer now, your custom trainings will be available for your future trainer to watch them\n\n" \
                                           "  Type training name"
    client_add_training_add_from_plan = "Choose a day from your plan"
    client_add_training_add_from_plan_no_plan = "Your trainer hasn't created a plan for you yet"

    client_add_from_plan_show_day = "Here are your exercises for day {}\n Select one of them to add it to your training"
    client_add_from_plan_show_exercise = "{}\n{} runs, {} repeats\nPersonal recommendation: {}\nType your working weight"
    client_add_from_plan_show_exercise_already_added = "You have already added this exercise into your training, please select another one or save training"
    client_add_from_plan_ask_video = "Do you want to add your own video where you showing how do you do this exercise?"
    client_add_from_plan_process_video = "Send me a video with your technique"
    client_add_from_plan_ask_for_save = "You have added next exercises from your plan:\n{}\nSelect one more or save training"
    client_add_from_plan_ask_for_question = "Do you want to leave a question about your technique? Your trainer will rely on it when will provide corrections"
    client_add_from_plan_process_client_note = "Type your question here"
    client_add_from_plan_process_save = "Saving exercises videos..."
    client_add_from_plan_process_sace_single_video = "Saveing video for exercise {}..."

    client_add_custom_start = "Type the name of the exercise or select one from your personal exercise list"
    client_add_custom_start_no_exercises = "You haven't added any exercise yet, type the name of the exercise"
    client_add_custom_process_num_runs = "Type the number of runs for exercise"
    client_add_custom_already_added = "You have already added this exercise to your training, create new one or select one from the list"
    client_add_custom_process_num_repeats = "Type the number of repeats per one run"
    client_add_custom_process_weight = "Type your working weight"

    client_fill_questionnaire = "Fill the questionnaire"
    client_custom_training_btn = "Custom training"
    client_from_plan_training_btn = "Training from plan"
    client_training_save_btn = "Save"

    client_number_required = "Type number pls"
    client_video_required = "I need a video file"

    file_too_big = "File too big. File size should be less than 50 Мb"

    multiple_files_alert = "You've sent multiple files, ony the first one will be processed"



    go_back_btn = "Go Back"
    next_action_btn = "Next"
    not_a_number_alert = "Please type number"