from aiogram.filters.callback_data import CallbackData


class SeePhotoActions:
    see_photo = 'see_photo'


class SeePhotoCallback(CallbackData, prefix='see_photo'):
    action: str


