from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.default_callbacks.default_callbacks import ChooseCallback
from app.workflows.registration.utils.callback_properties import ChooseUsrTypeOptions, RegistrationCallbackTargets
from app.entities.exercise.exercise import BodyPart, MuscleGroup, Exercise
from typing import Optional
from app.buttons.go_back import GoBackButton


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

    return builder.as_markup()


class ChooseKeyboard(InlineKeyboardBuilder):
    def __init__(self, target, options, option_attr, go_back_target, additional_buttons: list):
        super().__init__()
        for option in options:
            self.row(
                InlineKeyboardButton(
                    text=f'{option.name}', callback_data=ChooseCallback(
                        target=target,
                        option=f'{str(getattr(option, option_attr))}').pack()
                    )
                )
            if additional_buttons:
                for button in additional_buttons:
                    self.row(button)
            self.row(GoBackButton(text='Назад', target=go_back_target))











