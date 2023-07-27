from aiogram.filters.callback_data import CallbackData


class CreateTrainingCallback(CallbackData, prefix='create_training'):
    action: str


class CreateTrainingCallbackActions:
    create_training = 'create_training'
    decline = 'decline'
    save = 'save'


class ClientMainMenuTargets:
    create_training = 'create_training'
    show_training = 'show_training'


class ClientMainMenuOptions:
    new_training = 'new_training'
    show_training = 'show_training'

class ClientExerciseTargets:
    attach_video = 'attach_video'


