import asyncio
import os
from app.bot import dp, bot
import logging
from mongoengine import connect
from app.workflows.registration.handlers import registration_router
from app.workflows.client.handlers import client_router


logging.basicConfig(level=logging.INFO)

dp.include_router(registration_router)
dp.include_router(client_router)


async def main():
    connect("test", host="localhost", port=27017, username="myuser", password="mypassword")
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())