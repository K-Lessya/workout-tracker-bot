from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from ..callback_properties.targets import TrainerMyClientsTargets
from ..callback_properties.movetos import TrainerMainMenuMoveTo
from app.entities.single_file.models import Client
from ..callback_properties.movetos import MyCLientsMoveTo
from app.callbacks.callbacks import MoveCallback
from aiogram.types import InlineKeyboardButton
from app.config import CHOOSE_BUTTON_MAX_COUNT_PER_PAGE
from app.translations.base_translations import translations


class MyClientsKeyboard(InlineKeyboardBuilder):
    def __init__(self, clients: Client, start_index, lang):
        clients_list = []
        for client in clients:
            clients_list.append(client)
        super().__init__()
        if len(clients_list) <= CHOOSE_BUTTON_MAX_COUNT_PER_PAGE:
            for client in clients_list:
                self.row(InlineKeyboardButton(
                    text=f"{client.name} {client.surname}", callback_data=ChooseCallback(
                        target=TrainerMyClientsTargets.show_client,
                        option=f'{str(client.id)}').pack())
                )
        else:
            for client in clients_list[start_index:start_index+CHOOSE_BUTTON_MAX_COUNT_PER_PAGE:1]:
                self.row(InlineKeyboardButton(
                    text=f"{client.name} {client.surname}", callback_data=ChooseCallback(
                        target=TrainerMyClientsTargets.show_client,
                        option=f'{str(client.id)}').pack())
                )
            move_buttons = []
            if start_index > 0:
                move_buttons.append(
                    InlineKeyboardButton(
                        text="<<",
                        callback_data=MoveToCallback(move_to=MyCLientsMoveTo.show_prev_clients).pack()
                    )
                )
            if start_index+CHOOSE_BUTTON_MAX_COUNT_PER_PAGE-1 < len(clients_list)-1:
                move_buttons.append(
                    InlineKeyboardButton(
                        text=">>",
                        callback_data=MoveToCallback(move_to=MyCLientsMoveTo.show_next_clients).pack()
                    )
                )
            self.row(*move_buttons)
        self.row(InlineKeyboardButton(text=translations[lang].go_back_btn.value,
                                      callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu).pack()))


class SingleClientKeyboard(InlineKeyboardBuilder):
    def __init__(self, client: Client, lang):
        super().__init__()
        self.button(
            text=translations[lang].trainer_my_clients_single_clietn_menu_btn_questionnaire.value,
            callback_data=MoveCallback(target="to_no_content")
        )
        self.button(
            text=translations[lang].trainer_my_clients_single_clietn_menu_btn_trainings.value,
            callback_data=MoveCallback(target=MyCLientsMoveTo.show_trainings)
        )
        if not client.training_plan:
            self.button(
                text=translations[lang].trainer_my_clients_single_clietn_menu_btn_create_plan.value,
                callback_data=MoveToCallback(move_to=MyCLientsMoveTo.create_client_plan).pack()
            )
        else:
            self.button(
                text=translations[lang].trainer_my_clients_single_clietn_menu_btn_show_plan.value,
                callback_data=MoveCallback(target=MyCLientsMoveTo.show_client_plan_menu).pack()
            )
        self.button(
            text=translations[lang].go_back_btn.value,
            callback_data=MoveToCallback(move_to=TrainerMainMenuMoveTo.my_clients).pack()
        )
        self.adjust(2,1,1)


# class PlanDaysKeyboard(InlineKeyboardBuilder):
#     def __init__(self, num_days: int):
#         for i in range(1, num_days):
#             self.button(
#                 text=f'День {i}', callback_data=ChooseCallback(target=TrainerMyClientsTargets.choose_day, option=str(i))
#             )

class ClientQuizKeyboard(InlineKeyboardBuilder):
    def __init__(self, option):
        super().__init__()
        self.row(InlineKeyboardButton(text="Назад", callback_data=ChooseCallback(target=TrainerMyClientsTargets.show_client, option=option).pack()))