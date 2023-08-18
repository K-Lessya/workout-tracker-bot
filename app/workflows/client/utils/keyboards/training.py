from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from app.workflows.client.utils.callback_properties.movetos import ClientAddTrainingMoveTo
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, MoveToCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientMyPlanTargets
from app.workflows.client.utils.callback_properties.targets import ClientAddTrainingTargets
from app.workflows.client.utils.callback_properties.options import ClientAddTrainingOptions


class TrainingTypeKeyboard(InlineKeyboardBuilder):
    def __init__(self):
        super().__init__()
        self.button(text="Свободная тренировка",
                    callback_data=ChooseCallback(target=ClientAddTrainingTargets.choose_training_type,
                                                 option=ClientAddTrainingOptions.custom))
        self.button(text="Тренировка по плану",
                    callback_data=ChooseCallback(target=ClientAddTrainingTargets.choose_training_type,
                                                 option=ClientAddTrainingOptions.from_plan))
        self.button(text="Назад", callback_data=MoveToCallback(move_to=CommonGoBackMoveTo.to_client_main_menu))
        self.adjust(1,1)

