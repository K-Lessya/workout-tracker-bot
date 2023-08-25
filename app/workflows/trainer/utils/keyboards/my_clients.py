from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from ..callback_properties.targets import TrainerMyClientsTargets
from ..callback_properties.movetos import TrainerMainMenuMoveTo
from app.entities.single_file.models import Client
from ..callback_properties.movetos import MyCLientsMoveTo
from app.callbacks.callbacks import MoveCallback
from aiogram.types import InlineKeyboardButton


class MyClientsKeyboard(InlineKeyboardBuilder):
    def __init__(self, clients: Client):
        super().__init__()
        for client in clients:
            self.button(
                text=f"{client.name} {client.surname}", callback_data=ChooseCallback(
                    target=TrainerMyClientsTargets.show_client,
                    option=f'{str(client.id)}')
            )
        self.button(text=f"Назад", callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_trainer_main_menu))


class SingleClientKeyboard(InlineKeyboardBuilder):
    def __init__(self, client: Client):
        super().__init__()
        self.button(
            text="Анкета", callback_data=MoveCallback(target=MyCLientsMoveTo.client_quiz)
        )
        self.button(
            text="Тренировки", callback_data=MoveCallback(target=MyCLientsMoveTo.show_trainings)
        )
        if not client.training_plan:
            self.button(
                text="Составить план", callback_data=MoveToCallback(move_to=MyCLientsMoveTo.create_client_plan)
            )
        else:
            self.button(
                text="Тренировочный план", callback_data=MoveCallback(target="to_no_content")
            )
        self.button(
            text="Назад", callback_data=MoveToCallback(move_to=TrainerMainMenuMoveTo.my_clients)
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