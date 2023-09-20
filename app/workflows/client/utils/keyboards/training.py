from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from app.workflows.client.utils.callback_properties.movetos import ClientAddTrainingMoveTo
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.callbacks.callbacks import MoveCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientMyPlanTargets
from app.workflows.client.utils.callback_properties.targets import ClientAddTrainingTargets
from app.workflows.client.utils.callback_properties.options import ClientAddTrainingOptions
from app.translations.base_translations import translations


class TrainingTypeKeyboard(InlineKeyboardBuilder):
    def __init__(self, lang):
        super().__init__()
        self.button(text=translations[lang].client_custom_training_btn.value,
                    callback_data=ChooseCallback(target=ClientAddTrainingTargets.choose_training_type,
                                                 option=ClientAddTrainingOptions.custom))
        self.button(text=translations[lang].client_from_plan_training_btn.value,
                    callback_data=ChooseCallback(target=ClientAddTrainingTargets.choose_training_type,
                                                 option=ClientAddTrainingOptions.from_plan))
        self.button(text=translations[lang].go_back_btn.value, callback_data=MoveCallback(target=CommonGoBackMoveTo.to_client_main_menu))
        self.adjust(1,1)

