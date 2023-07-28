from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..default_callbacks.default_callbacks import TestCallback,TestTasks
from app.entities.single_file.models import Client, Trainer
from app.entities.single_file.crud import *


def create_tester_keyboard(testers_id: list[int]):
    builder = InlineKeyboardBuilder()
    for tester_id in testers_id:
        if get_client_by_id(tg_id=tester_id):
            client = get_client_by_id(tg_id=tester_id)
            builder.button(text=f'Delete client user {client.name} {client.surname}',
                           callback_data=TestCallback(test_task=TestTasks.delete_me, user=str(client.tg_id)))
        if get_trainer(tg_id=tester_id):
            trainer = get_trainer(tg_id=tester_id)
            builder.button(text=f'Delete trainer user {trainer.name} {trainer.surname}',
                           callback_data=TestCallback(test_task=TestTasks.delete_me, user=str(trainer.tg_id)))
    builder.adjust(1, 1)
    return builder.as_markup()
