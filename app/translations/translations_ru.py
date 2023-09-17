from enum import Enum


class RussianTranslations(Enum):
    user_type_question = 'Привет, регистрируемся как тренер или как клиент?'
    main_menu_text = 'Привет снова! Давай продолжим работу, выбери один из пунктов меню'
    already_added_client_welcome_message_1 = 'Привет ты был добавлен в систему тренером '
    already_added_client_welcome_message_2 = ', давай заполним твой профиль, введи свое имя'
    finish_registration_alert = 'Необходимо закончить текущую регистрацию'
    registration_ask_name_trainer = "Привет новый тренер, введи свое имя"
    registration_ask_name_client = "Привет, введи свое имя"
    registration_already_registered_trainer = "Ты уже зарегистрирован как тренер"
    registration_already_registered_client = "Ты уже зарегистрирован как клиент"
    registration_process_name = "Отлично {}, а теперь введи свою фамилию"
    registration_process_photo_question = "Отлично {}, а хочешь загрузить фото?"
    registration_process_photo = "Тогда присылай свое лучшее фото!"
    registration_alert_waiting_for_photo = "Я ожидаю фото"
    registration_visibility_question_trainer = "Хочешь ли то чтобы твой профиль был виден клиентам?"
    registration_visibility_question_client = "Хочешь ли то чтобы твой профиль был виден тренерам?"
    registration_finish_client = 'Добро пожаловать в меню клиента, тут ты можешь добавлять тренировки и' \
                                 ' просмотривать информацию о уже добавленных тренировках'
    registration_finish_trainer = 'Добро пожаловать в меню тренера, тут ты можешь добавлять план тренировок для клиентов и ' \
                                  'просмотривать информацию о уже добавленных тренировках'

    use_btn_alert = "Воспользуйся одной из кнопок"
    usr_type_btn_client = "Клиент"
    usr_type_btn_trainer = "Тренер"
    yes_no_btn_yes = "Да"
    yes_no_btn_no = "Нет"

    client_menu_btn_add_training = "Добавить тренировку"
    client_main_menu_btn_my_requests = "Мои заявки({})"
    client_main_menu_btn_my_trainings = "Мои тренировки"
    client_main_menu_btn_my_trainer = "Мой тренер"
    client_main_menu_btn_my_plan = "Мой план"



    trainer_add_client_menu_choose_add_method = "Выбери как ты хочешь добавить клиента"
    trainer_add_client_menu_share_contact = "Тогда поделись со мной контактом твоего клиента и я добавлю его," \
                                            " ты увидишь его когда он завершит процесс регистрации"
    trainer_add_client_menu_already_registered_as_trainer = "Этот человек зарегистрирован как тренер, ты не " \
                                                       "можешь доавить его как клиента"
    trainer_add_client_menu_client_already_added = "У тебя уже есть такой клиент"
    trainer_add_client_menu_client_already_has_another_trainer = "Этот клиент уже занят"
    trainer_add_client_menu_client_added_successfully = "Клиент добавлен"
    trainer_add_client_menu_select_from_list = "Выбери клиента из списка"
    trainer_add_client_menu_all_clients_already_have_trainer = "Все доступные клиенты уже заняты"
    trainer_add_client_menu_add_client_profile = "Имя: {}\nФамилия: {}\nДобавить этого клиента?"
    trainer_add_client_menu_request_sent = "Клиенту отпралвена заявка"
    trainer_add_client_menu_request_text = "Тебе поступило новое предложение от тренера, посмотри его"
    trainer_add_client_menu_watch_others = "Хорошо, посмотрим других"
    trainer_add_client_menu_back_to_main_menu = "Мы снова в главном меню"


    trainer_main_menu_btn_add_client = "Добавить клиента"
    trainer_main_menu_btn_my_clients = "Мои клиенты"
    trainer_main_menu_btn_exercise_db = "База упражнений"
    trainer_main_menu_btn_questionaire = "Анкета для клиентов"
    trainer_add_client_btn_share_contact = "Поделиться контактом"
    trainer_add_client_btn_select_existed = "Добавить из уже зарегистрированных клиентов"





    go_back_btn = "Назад"


