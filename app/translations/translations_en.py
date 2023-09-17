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



    trainer_main_menu_btn_add_client = "Add client"
    trainer_main_menu_btn_my_clients = "My clients"
    trainer_main_menu_btn_exercise_db = "Exercises database"
    trainer_main_menu_btn_questionaire = "Questionnaire for clients"
    trainer_add_client_btn_share_contact = "Share contact"
    trainer_add_client_btn_select_existed = "Add from already registered clients"



    go_back_btn = "Go Back"