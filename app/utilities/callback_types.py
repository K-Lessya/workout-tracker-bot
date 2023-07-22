from aiogram.filters.callback_data import CallbackData


class ChooseCallbackTargets:
    usr_type = 'usr_type'
    process_photo = 'process_photo'
    process_visibility = 'process_visible'


class ChooseCallbackOptions:
    trainer = 'trainer'
    client = 'client'


class YesNoOptions:
    yes = 'yes'
    no = 'no'


class ChooseCallback(CallbackData, prefix='choose'):
    target: str
    option: str


class SeePhotoActions:
    see_photo = 'see_photo'


class SeePhotoCallback(CallbackData, prefix='see_photo'):
    action: str


