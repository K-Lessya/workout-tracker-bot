import asyncio
import os
from app.bot import dp, bot
import logging
from mongoengine import connect
from app.workflows.client.router import client_router
from app.workflows.trainer.router import trainer_router
from app.workflows.common.router import common_router
from app.handlers.main_router import main_router
from app.config import MONGO_CONNECTION_STRING, TESTER_ID
from app.entities.single_file.models import Client, Trainer, ClientRequests
from app.entities.single_file.crud import get_client_by_id, get_trainer

logging.basicConfig(level=logging.DEBUG)

dp.include_router(main_router)
dp.include_router(client_router)
dp.include_router(trainer_router)
dp.include_router(common_router)

mock_client_id = 23432565
mock_trainer_id = TESTER_ID


async def main():
    # connect("test", host="localhost", port=27017, username="myuser", password="mypassword")
    print(MONGO_CONNECTION_STRING)
    connect(host=MONGO_CONNECTION_STRING)
    if not get_trainer(mock_trainer_id):
        trainer = Trainer(tg_id=mock_trainer_id, name='test trainer', surname='test trainer', photo_link='defaults/no-user-image-icon-0.png', visibility=True)
        trainer.save()
        if not get_client_by_id(mock_client_id) or not get_client_by_id(mock_trainer_id):
            client = Client(tg_id=mock_client_id, name="test client", surname='test client', photo_link='defaults/no-user-image-icon-0.png', visibility=True, trainer=trainer)
            client.save()
            client_request = ClientRequests(client=client, trainers=[])
            client_request.save()
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())