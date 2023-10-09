from enum import Enum


class RussianTranslations(Enum):
    user_type_question = 'Привет, регистрируемся как тренер или как клиент?'
    main_menu_text = 'Привет снова! Давай продолжим работу, выбери один из пунктов меню'
    already_added_client_welcome_message_1 = 'Привет, ты был добавлен в систему тренером '
    already_added_client_welcome_message_2 = ', давай заполним твой профиль, введи свое имя'
    finish_registration_alert = 'Необходимо закончить текущую регистрацию'
    registration_ask_name_trainer = "Привет, новый тренер, введи свое имя"
    registration_ask_name_client = "Привет, введи свое имя"
    registration_already_registered_trainer = "Ты уже зарегистрирован как тренер"
    registration_already_registered_client = "Ты уже зарегистрирован как клиент"
    registration_process_name = "Отлично, {}, а теперь введи свою фамилию"
    registration_process_photo_question = "Отлично, {}, а хочешь загрузить фото?"
    registration_process_photo = "Тогда присылай свое лучшее фото!"
    registration_alert_waiting_for_photo = "Я ожидаю фото"
    registration_visibility_question_trainer = "Хочешь ли ты, чтобы твой профиль был виден клиентам?"
    registration_visibility_question_client = "Хочешь ли ты, чтобы твой профиль был виден тренерам?"
    registration_finish_client = 'Добро пожаловать в меню клиента, тут ты можешь добавлять тренировки и' \
                                 ' просматривать информацию об уже добавленных тренировках'
    registration_finish_trainer = 'Добро пожаловать в меню тренера, тут ты можешь добавлять план тренировок для клиентов и ' \
                                  'просматривать информацию об уже добавленных тренировках'


    usr_type_btn_client = "Клиент"
    usr_type_btn_trainer = "Тренер"


    client_menu_btn_add_training = "Добавить тренировку"
    client_main_menu_btn_my_requests = "Мои заявки({})"
    client_main_menu_btn_my_trainings = "Мои тренировки"
    client_main_menu_btn_my_trainer = "Мой тренер"
    client_main_menu_btn_my_plan = "Мой план"



    trainer_add_client_menu_choose_add_method = "Выбери как ты хочешь добавить клиента"
    trainer_add_client_menu_share_contact = "Тогда поделись со мной контактом твоего клиента и я добавлю его," \
                                            " ты увидишь его, когда он завершит процесс регистрации"
    trainer_add_client_menu_already_registered_as_trainer = "Этот человек зарегистрирован как тренер, ты не " \
                                                       "можешь доавить его как клиента"
    trainer_add_client_menu_client_already_added = "У тебя уже есть такой клиент"
    trainer_add_client_menu_client_already_has_another_trainer = "Этот клиент уже занят"
    trainer_add_client_menu_client_added_successfully = "Клиент добавлен"
    trainer_add_client_menu_select_from_list = "Выбери клиента из списка"
    trainer_add_client_menu_all_clients_already_have_trainer = "Все доступные клиенты уже заняты"
    trainer_add_client_menu_add_client_profile = "Имя: {}\nФамилия: {}\nДобавить этого клиента?"
    trainer_add_client_menu_request_sent = "Клиенту отправлена заявка"
    trainer_add_client_menu_request_text = "Тебе поступило новое предложение от тренера, посмотри его"
    trainer_add_client_menu_watch_others = "Хорошо, посмотрим других"
    trainer_add_client_menu_back_to_main_menu = "Мы снова в главном меню"

    trainer_add_exercise_choose_body_part = 'Введи название части тела, на которую делается упражнение, или выбери из существующих'
    trainer_add_exercise_create_muscle_group_message = 'Теперь введи группу мыщц для которой предназначено это упражнение'
    trainer_add_exercise_create_muscle_group_callback = 'Теперь введи группу мыщц для которой предназначено это упражнение' \
                                                        'или снова выбери ее из списка'
    trainer_add_exercise_type_exercise_name = "А теперь введи название упражнения"
    trainer_add_exercise_ask_for_media = "Хочешь загрузить фотографию или видео с техникой упражнения?"
    trainer_add_exercise_process_media = 'Тогда присылай фото или видео техники выполнения.\n' \
                                         'Желательно, чтобы на фото были два крайних положения' \
                                         ' при выполнении упражнения.'
    trainer_add_exercise_process_media_text_recieved = "Мне нужно прислать фото или видео"
    trainer_add_exercise_process_media_file_size_alert = "Размер файла слишком большой, пожалуйста, присылай файлы не больше 50Мб"
    trainer_add_exercise_ask_for_save = 'Давай все проверим.\nЧасть тела: {}\nГруппа мышц:' \
                                         ' {}\nНазвание: {}\n Сохранить?'
    trainer_add_exercise_process_save_loading = "Сохраняю упражнение..."
    trainer_add_exercise_process_save_process_file = "Обрабатываю файл..."
    trainer_add_exercise_process_save_upload_file = "Загружаю файл..."
    trainer_add_exercise_process_save_file_uploaded = "Файл загружен"
    trainer_add_exercise_process_save_process_bp_mg = "Обрабатываю части тела и группы мыщц..."
    trainer_add_exercise_process_save_not_saved = "Упражнение не сохранено"

    trainer_exercise_db_choose_bodypart = "Давай выберем упражнения"
    trainer_exercise_db_menu_choose_body_part = 'Давай выберем на какую часть тела хочешь просмотреть упражнения,' \
                                     ' если частей тела нет, то создай новое упражнение'
    trainer_exercise_db_menu_choose_muscle_group = "Выбери группу мышц"
    trainer_exercise_db_menu_choose_exercise = "Выбери упражнение"
    trainer_exercise_db_menu_sending_exercie_media = "Присылаю файл упражнения"
    trainer_exercise_db_menu_inline_create_body_part = "Данное сообщение воспринимается как процесс создания упражнения(части тела)\n" \
                                                       "Часть тела {} " \
                                                       "А теперь введи название группы мышц"
    trainer_exercise_db_menu_inline_create_muscle_group = "Данное сообщение воспринимается как процесс создания упражнения(группы мышц)\n" \
                                                          "Часть тела {}\n" \
                                                          "Группа мышц {}\n" \
                                                          "А теперь введи название упражнения"
    trainer_exercise_db_menu_inline_create_exercise = 'Данное сообщение воспринято как создание нового упражнения (Названия упражнения)' \
                                                      'Хочешь загрузить фотографию или видео с техникой упражнения?'


    trainer_choose_language = "Выбери язык"



    trainer_my_clients_menu_my_clients = "Мои клиенты. Выбирай нужного"
    trainer_my_clients_menu_no_clients_registered = "Ни один из клиентов пока не зарегистрировался или не принял заявку"
    trainer_my_clients_menu_no_clients = "У тебя пока нет клиентов"
    trainer_my_clients_menu_single_client_menu = "Клиент:\nИмя: {}\nФамилия: {}"

    trainer_my_clients_menu_single_client_create_plan_start = "Составляем план для клиента {} {}.\n" \
                                                              "Можешь добавить день или отредактировать уже существующий"
    trainer_my_clients_menu_single_client_create_plan_day_name = "Введи название дня {}"
    trainer_my_clients_menu_single_client_create_plan_select_exercise = "Давай выберем упражнения для дня {}, либо создадим новые"
    trainer_my_clients_menu_single_client_create_plan_no_exercises = "Пока в твоей базе нет упражнений, давай добавим их"
    trainer_my_clients_menu_single_client_create_plan_add_trainer_note = "Добавь свой комментарий или рекомендацию по" \
                                                                         " технике выполнения(Это общая " \
                                                                         "подсказка, которая будет выводиться " \
                                                                         "вместе с упражнением), либо нажми далее"
    trainer_my_clients_menu_single_client_create_plan_append_trainer_note = "Напиши дополнение к своему комментарию, оно будет добавлено к текущему"


    trainer_my_clietns_menu_single_client_create_plan_exercise_already_added = "Ты уже добавил это упражнение в план, выбери другое"
    trainer_my_clietns_menu_single_client_create_plan_add_num_runs = "Введи количество подходов"
    trainer_my_clietns_menu_single_client_create_plan_add_num_repeats = "Введи количество повторений за подход"
    trainer_my_clietns_menu_single_client_create_plan_trainer_note_was_not_added = "Тренер не добавил примечание"
    trainer_my_clietns_menu_single_client_create_plan_add_one_more_or_save_day = "Отлично, теперь давай добавим следующее упражнение, либо сохраним день"
    trainer_my_clients_menu_single_clietn_create_plan_save_client_notification = "{} {} только что составил для тебя план тренировок, можешь его посмотреть"
    trainer_my_clients_menu_single_clietn_create_plan_save_trainer_alert = "План сохранен, клиент может его просмотреть, ему отправлено уведомление"
    trainer_my_clients_menu_single_clietn_create_plan_save_plan_question = "Сохранить план?"
    trainer_my_clients_menu_single_client_publish_plan = "Опубликовать план у клиента"
    trainer_my_clients_menu_single_client_publish_plan_notification = "План опубликован и заменит текущий, если он есть"

    trainer_my_clients_edit_plan_exercise_change_exercise = "Заменить упражнение"
    trainer_my_clients_edit_plan_exercise_change_runs = "Изменить количество подходов"
    trainer_my_clients_edit_plan_exercise_change_repeats = "Изменить количество повторений за подход"
    trainer_my_clients_edit_plan_exercise_change_trainer_note = "Изменить примечание"
    trainer_my_clients_edit_plan_exercise_append_trainer_note = "Дополнить комментарий"

    trainer_my_clients_menu_single_client_plan_menu = "Выбери: просмотреть план или cоздать новый план"
    trainer_my_clients_menu_single_client_vieew_plan_show_days = "Выбери день из плана"
    trainer_my_clients_menu_single_client_vieew_plan_show_exercises = "Выбери упражнение"
    trainer_my_clients_menu_single_client_view_plan_load_data = "Загружаю данные..."
    trainer_my_clients_menu_single_client_view_plan_send_photo = "Отправляю фото..."
    trainer_my_clients_menu_single_client_view_plan_get_video = "Получаю видео..."
    trainer_my_clients_menu_single_client_view_plan_send_video = "Отправляю видео..."

    trainer_my_clients_menu_single_client_view_trainings_no_trainings = "Клиент еще не добавил тренировку"
    trainer_my_clients_menu_single_client_view_trainings_choose_day = "Выбери тренировку из списка"
    trainer_my_clients_menu_single_client_view_trainings_show_training = "Тренировка {}\nДата: {}\nУпражнения:"

    trainer_my_clients_menu_single_client_view_trainings_show_exercise = "Упражнение: {}\n" \
                                                                         "Количество: {}x{}\n" \
                                                                         "Вес с которым работал: {} кг"
    trainer_my_clients_menu_single_client_view_trainings_update_comment = "Обновить комментарий"
    trainer_my_clients_menu_single_client_view_trainings_create_comment = "Добавить комментарий"
    trainer_my_clients_menu_single_client_view_trainings_append_comment = "Дополнить комментарий"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_video = "Пометка клиента:\n{}\n\nКомментарий:\n{}"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_video_no_comment = "Пометка клиента:\n {}\n\nКомментарий отсутствует"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_as_for_comment = "Напиши свой комментарий к видео"
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_as_for_append_comment = 'Дополни свой комментарий'
    trainer_my_clients_menu_single_client_view_trainings_show_exercise_comment_saved = "Комментарий сохранен"


    trainer_create_plan_choose_exercise_for_day = "Давай выберем упражнения для дня {}"

    trainer_create_plan_add_trainer_note = 'Добавь свой комментарий или рекомендацию по технике выполнения' \
                                           '(Это общая подсказка, которая будет выводиться вместе с упражнением)'

    ask_from_add_training_notification = 'Уведомить тренера о добавленной тренировке?'
    new_training_notification = '{} {} только что добавил тренировку'
    open_training_from_notification = "Просмотреть тренировку"
    skip_training_notification = 'Пропустить'
    skip_training_notification_alarm = 'Ты все еще можешь просмотреть тренировку в профиле клиента'

    trainer_main_menu_btn_add_client = "Добавить клиента"
    trainer_main_menu_btn_my_clients = "Мои клиенты"
    trainer_main_menu_btn_exercise_db = "База упражнений"
    trainer_main_menu_btn_questionaire = "Анкета для клиентов"
    trainer_main_menu_btn_change_language = "Сменить язык"
    trainer_add_client_btn_share_contact = "Поделиться контактом"
    trainer_add_client_btn_select_existed = "Добавить из уже зарегистрированных клиентов"

    trainer_my_clients_single_clietn_menu_btn_questionnaire = "Анкета"
    trainer_my_clients_single_clietn_menu_btn_trainings = "Тренировки"
    trainer_my_clients_single_clietn_menu_btn_create_plan = "Составить план"
    trainer_my_clients_single_clietn_menu_btn_show_plan = "Планы тренировок"

    trainer_my_clients_single_client_create_plan_menu = "Добавить день в план"

    trainer_exercise_plan_list_keyboard_save_day = "Вернуться к добавленным в день упражнениям"
    trainer_exercise_plan_list_keyboard_add_exercise = "Добавить упражнение"

    trainer_client_plan_menu_keyboard_show_plan = "Просмотреть план"
    trainer_client_plan_menu_keyboard_create_new_plan = "Создать новый план"

    trainer_client_plan_days_keyboard_day_btn = "День {}({})"

    trainer_client_training_exercise_show_video_with_comments = "Показать видео с комментариями"


    trainer_add_exercise_btn_add_exercise = "Добавить упражнение"

    trainer_create_plan_notification = "Все изменения и добавления сохраняются автоматически\nТы сможешь вернуться к редактированию в любой момент, если решишь прервать создание плана"
################## Client ########################
    client_main_menu = "Меню клиента"

    client_my_trainer = "Имя: {}\nФамилия: {}"
    client_my_trainer_no_trainer = "У тебя еще нет тренера"

    client_requests_menu = "Входящие заявки от тренеров"
    client_requests_show_request = "Заявка от тренера:\n{} {}\nПринять заявку?"
    client_requests_accept_request = "Поздравляю, теперь {} {} тренирует тебя"
    client_requests_accept_request_trainer_notification = "{} {} принял твою заявку, теперь ты сможешь увидеть его в списке клиентов"
    client_requests_decline_request = "Заявка от {} {} была удалена"
    client_requests_decline_request_trainer_notification = "{} {} отклонил твою заявку"

    client_my_plan_loading_data = "Загружаю данные"
    client_my_plan_choose_day = "Выбери день"
    client_my_plan_show_day = "Вот твои упражнения для дня {}\n Если не знаешь как выполнять, просто выбери упражнение из списка"
    client_my_plan_loading_video = "Загружаю файл"
    client_my_plan_show_exercise = "{}\n{} подхода по {} раз(а)\nПримечание: {}"

    client_my_trainings_choose_training = "Выбирай день тренировки"
    client_my_trainings_show_training = "Тренировка {}\nДата: {}\nУпражнения:"
    client_my_trainings_show_exercise = "Упражнение: {}\nКоличество: {}x{}\nВес с которым работал: {} кг"
    client_my_trainings_show_video_client_comment = "Мой комментарий: {}\n"
    client_my_trainings_show_video_no_client_comment = "Ты не оставил комментарий\n"
    client_my_trainings_show_video_trainer_comment = "Комментарий тренера: {}"
    client_my_trainings_show_video_no_trainer_comment = "Комментарий тренера отсутствует"

    client_add_training_choose_training = "Хочешь добавить собственную тренировку или из плана"
    client_add_training_add_custom_start = "  Упражнения для свободной тренировки создаешь ты сам, поэтому тебе не будут доступны:\n\n"\
                                         "- Упражнения, которые могут использовать тренера\n"\
                                         "- Описания упражнений и материалы показывающие технику\n"\
                                         "- Индивидуальные рекомендации к упражнениям от тренеров\n"\
                                         "  Все эти материалы доступны только если ты занимаешься по плану, который составил тебе тренер\n\n"\
                                         "  Ты все еще можешь оставлять видео своего выполнения упражнений, и тренер(если он у тебя есть) сможет дать комментарий по технике\n\n"\
                                         "  Если сейчас тренера у тебя нет, то, когда он появится, он сможет просмотреть все твои свободные тренировки и дать по ним комментарий\n\n"\
                                         "  Введи название своей тренировки"
    client_add_training_add_from_plan = "Выбери день из плана"
    client_add_training_add_from_plan_no_plan = "Тренер еще не составил для тебя план"


    client_add_from_plan_show_day =  "Вот твои упражнения для дня {}\n Если не знаешь как выполнять, просто выбери упражнение из списка"
    client_add_from_plan_show_exercise = "{}\n{} подхода по {} раз(а)\nПримечание: {}\nВведи вес с которым работал"
    client_add_from_plan_show_exercise_already_added = "Ты уже добавил это упражнение, выбери другое"
    client_add_from_plan_ask_video = "Отлично, хочешь добавить видео?"
    client_add_from_plan_process_video = "Присылай видео своего выполнения"
    client_add_from_plan_ask_for_save = "Ты добавил следующие упражнения из плана:\n{}\nВыбирай упражнение"
    client_add_from_plan_ask_for_question = "Хочешь оставить свой собственный комментарий или вопрос к видео для тренера?"
    client_add_from_plan_process_client_note = "Напиши свой вопрос или комментарий, тренер сможет его увидеть"
    client_add_from_plan_process_save = "Сохраняю видео упражнения"
    client_add_from_plan_process_sace_single_video = "Сохраняю видео для упражнения {}"

    client_add_custom_start = "Теперь введи название первого упражнения или выбери из уже созданных тобой упражнений"
    client_add_custom_start_no_exercises = "У тебя еще нет своих упражнений, введи название первого"
    client_add_custom_process_num_runs = "А теперь введи количество подходов"
    client_add_custom_already_added = "Ты уже добавил это упражнение в тренировку, выбери другое или создай новое"
    client_add_custom_process_num_repeats = "Хорошо, а теперь введи количество повторений за подход"
    client_add_custom_process_weight = "Хорошо, а теперь введи вес с которым работал"


    client_fill_questionnaire = "Заполнить анкету"
    client_custom_training_btn = "Свободная тренировка"
    client_from_plan_training_btn = "Тренировка по плану"
    client_training_save_btn = "Сохранить"



    client_number_required = "Нужно ввести число"
    client_video_required = "Необходимо прислать видео"

    file_too_big = "Размер файла слишком большой, пожалуйста, присылай файлы размером до 50 Мб"













    yes_no_btn_yes = "Да"
    yes_no_btn_no = "Нет"
    go_back_btn = "Назад"
    next_action_btn = "Далее"
    use_btn_alert = "Воспользуйся одной из кнопок"




    multiple_files_alert = "Ты прислал больше одного файла, обработан будет первый"
    not_a_number_alert = "Я ожидаю число"


