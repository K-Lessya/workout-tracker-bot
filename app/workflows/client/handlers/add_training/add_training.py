import os
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.entities.exercise.crud import get_all_exercises
from app.utilities.default_callbacks.default_callbacks import ChooseCallback, YesNoOptions, MoveToCallback
from app.workflows.client.utils.callback_property import CreateTrainingCallback, CreateTrainingCallbackActions, ClientMainMenuTargets,\
    ClientMainMenuOptions, ClientExerciseTargets

from app.workflows.client.utils.states import ClientStates
from app.bot import bot
from app.workflows.client.utils.keyboards.training import TrainingTypeKeyboard
from app.entities.single_file.models import Training, ClientTrainingExercise
from app.entities.single_file.crud import create_training, get_client_by_id, get_trainer
from app.workflows.client.utils.keyboards.client_main_menu import create_client_main_menu_keyboard
from app.workflows.client.utils.keyboards.create_trainings import create_add_exercise_keyboard
from app.utilities.default_keyboards.yes_no import create_yes_no_keyboard
from app.s3.uploader import upload_file
from datetime import date
from app.workflows.client.utils.callback_properties.movetos import ClientMainMenuMoveTo
from app.workflows.client.utils.callback_properties.targets import ClientAddTrainingTargets
from app.workflows.client.utils.callback_properties.options import ClientAddTrainingOptions
from app.entities.training_plan.crud import get_training_days, get_client_active_plans
from app.workflows.client.utils.keyboards.training_plan import TrainingDaysKeyboard
from app.workflows.client.handlers.add_training.from_plan import training_from_plan_router
from app.callbacks.callbacks import MoveCallback
from app.workflows.common.utils.callback_properties.movetos import CommonGoBackMoveTo
from app.utilities.helpers_functions import callback_error_handler
from app.entities.single_file.crud import get_client_by_id
from app.translations.base_translations import translations

add_training_router = Router()
add_training_router.include_routers(training_from_plan_router)

@add_training_router.callback_query(MoveCallback.filter(F.target == ClientMainMenuMoveTo.add_training))
@callback_error_handler# Create training flow
async def start_creating_training(callback: CallbackQuery, callback_data: MoveToCallback, state: FSMContext):
            await state.set_state(ClientStates.add_training.process_training_type)
            client = get_client_by_id(callback.from_user.id)
            lang = client.lang
            await state.update_data({'lang': lang})
            await callback.message.edit_text(translations[lang].client_add_training_choose_training.value,
                                             reply_markup=TrainingTypeKeyboard(lang).as_markup())



@add_training_router.callback_query(ChooseCallback.filter(F.target == ClientAddTrainingTargets.choose_training_type))
@callback_error_handler
async def process_training_type(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    if callback_data.option == ClientAddTrainingOptions.custom:
        await state.set_state(ClientStates.add_training.add_custom.process_training_name)
        await callback.message.edit_text(translations[lang].client_add_training_add_custom_start.value)

    elif callback_data.option == ClientAddTrainingOptions.from_plan:
        active_plans = get_client_active_plans(callback.from_user.id)
        if active_plans:
            plan = active_plans[0]
            training_days = plan.days
            await state.update_data({"training_days": training_days})
            await state.set_state(ClientStates.add_training.add_from_plan.show_plan)
            await callback.message.edit_text(translations[lang].client_add_training_add_from_plan.value,
                                             reply_markup=TrainingDaysKeyboard(training_days,
                                                                               target=ClientAddTrainingTargets.show_day,
                                                                               lang=lang,
                                                                               go_back_target=CommonGoBackMoveTo.to_client_main_menu).as_markup())
        else:
            await callback.answer(translations[lang].client_add_training_add_from_plan_no_plan.value, show_alert=True)



@add_training_router.callback_query(ChooseCallback.filter(F.target == 'send-training-notification'))
@callback_error_handler
async def send_notifications(callback: CallbackQuery, callback_data: ChooseCallback, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get('lang')
    client = get_client_by_id(callback.from_user.id)
    trainer_id = client.trainer.tg_id
    if callback_data.option == YesNoOptions.yes:
        await bot.send_message(chat_id=trainer_id, text="текст уведомления")

