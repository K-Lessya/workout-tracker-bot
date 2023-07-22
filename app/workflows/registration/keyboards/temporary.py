from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from app.utilities.callback_types import ChooseCallback, ChooseCallbackOptions, YesNoOptions, ChooseCallbackTargets, SeePhotoCallback,SeePhotoActions


def create_see_photo_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пришли мне фото мое", callback_data=SeePhotoCallback(action=SeePhotoActions.see_photo)
    )
    return builder.as_markup()