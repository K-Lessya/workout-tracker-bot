import asyncio
import os
from app.bot import dp, bot
import logging
from mongoengine import connect
from app.workflows.client.router import client_router
from app.workflows.trainer.router import trainer_router
from app.workflows.common.router import common_router
from app.handlers.main_router import main_router
from app.config import MONGO_CONNECTION_STRING

logging.basicConfig(level=logging.DEBUG)

dp.include_router(main_router)
dp.include_router(client_router)
dp.include_router(trainer_router)
dp.include_router(common_router)


async def main():
    # connect("test", host="localhost", port=27017, username="myuser", password="mypassword")
    print(MONGO_CONNECTION_STRING)
    connect(host=MONGO_CONNECTION_STRING)
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())