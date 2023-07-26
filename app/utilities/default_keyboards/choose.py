from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions, RegistrationCallbackTargets
from app.entities.exercise.exercise import BodyPart, MuscleGroup, Exercise
from typing import Optional


def create_choose_keyboard(target: Optional[str], options: Optional[list], option_attr: Optional[str],
                           additional_buttons: list[InlineKeyboardButton]):
    builder = InlineKeyboardBuilder()
    if options:
        for option in options:
            print(getattr(option, option_attr))
            builder.row(InlineKeyboardButton(
                text=f"{option.name}", callback_data=ChooseCallback(
                    target=target,
                    option=f'{str(getattr(option, option_attr))}').pack()
            ))
    builder.row(*additional_buttons)



#         InlineKeyboardButton(text=f'Добавить упражнение',
#                                      callback_data=ChooseCallback(target=target,
#                                                                  option=ListBodyPartsOptions.add_pure_exercise).pack()),
#         InlineKeyboardButton(text=f"Назад", callback_data=ChooseCallback(target=TrainerMainMenuTargets.go_to_main_menu,
#                                                                          option='').pack())
# )

    return builder.as_markup()

