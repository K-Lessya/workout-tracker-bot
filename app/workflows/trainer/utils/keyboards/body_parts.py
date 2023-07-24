from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.choose_callback import ChooseCallback
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions, RegistrationCallbackTargets
from ..callback_properties import TrainerAddClientTargets,ListBodyPartsTargets, TrainerMainMenuTargets,\
    ListBodyPartsOptions
from app.entities.exercise.exercise import BodyPart


def create_show_body_parts_keyboard(body_parts: list[BodyPart]):
    builder = InlineKeyboardBuilder()
    for body_part in body_parts:
        builder.row(InlineKeyboardButton(
            text=f"{body_part.name}", callback_data=ChooseCallback(
                target=ListBodyPartsTargets.show_body_part,
                option=f'{body_part.name}').pack()
        ))
    builder.row(InlineKeyboardButton(text=f'Добавить упражнение',
                                     callback_data=ChooseCallback(target=ListBodyPartsTargets.add_exercise,
                                                                 option=ListBodyPartsOptions.add_pure_exercise).pack()),
        InlineKeyboardButton(text=f"Назад", callback_data=ChooseCallback(target=TrainerMainMenuTargets.go_to_main_menu,
                                                                        option='').pack())
)

    return builder.as_markup()

