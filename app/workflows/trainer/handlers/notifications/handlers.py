from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.callbacks.callbacks import TrainingNotificationCallback
from app.callbacks.targets.notifications import TrainingNotificationTargets
from app.entities.single_file.crud import get_client_by_id, get_client_training, get_trainer
from app.keyboards.trainings.keyboard import TrainingExercisesKeyboard
from app.translations.base_translations import translations
from app.utilities.helpers_functions import callback_error_handler
from app.workflows.trainer.utils.callback_properties.movetos import MyCLientsMoveTo
from app.workflows.trainer.utils.callback_properties.targets import TrainerMyClientsTargets
from app.workflows.trainer.utils.states import TrainerStates

training_notifications_router = Router()


@training_notifications_router.callback_query(TrainingNotificationCallback.filter(F.target == TrainingNotificationTargets.open_training))
@callback_error_handler
async def open_client_training_from_notification(callback: CallbackQuery, callback_data: TrainingNotificationCallback, state: FSMContext):
    client_id = int(callback_data.client_id)
    await state.update_data({'client': client_id})
    training_id = int(callback_data.training_id)
    formatted_date_string = '%d/%m/%Y'
    state_data = await state.get_data()
    client_id = state_data['client']
    client = get_client_by_id(client_id)
    lang = state_data.get('lang', get_trainer(callback.from_user.id).lang)
    await state.update_data({'lang': lang})
    await state.set_state(TrainerStates.my_clients.client_training.working_with_menu)
    training = get_client_training(tg_id=client.tg_id, training_id=training_id)
    training_name = training.name
    exercises = training['training_exercises']
    await state.update_data({'training_exercises': exercises, 'training_id': training_id})
    await callback.message.edit_text(
        text=translations[lang].trainer_my_clients_menu_single_client_view_trainings_show_training
            .value.format(training_name, training.date.strftime(formatted_date_string)),
        reply_markup=TrainingExercisesKeyboard(target=TrainerMyClientsTargets.show_training_exercise,
                                               go_back_target=MyCLientsMoveTo.show_trainings,
                                               exercises=exercises,
                                               lang=lang).as_markup())



@training_notifications_router.callback_query(TrainingNotificationCallback.filter(F.target == TrainingNotificationTargets.skip_training))
@callback_error_handler
async def skip_training_notification(callback: CallbackQuery, callback_data: TrainingNotificationCallback, state: FSMContext):
    await callback.message.delete()