import asyncio
import logging
import sys

from app import database
from app.config import Telegram
from app.handlers import router

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode


dp = Dispatcher()


async def run_bot() -> None:
    await database.connect()

    bot = Bot(Telegram.TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await database.disconnect()
        await dp.stop_polling()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(run_bot())
