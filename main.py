import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import basic_handlers, work_handlers
from parsing_bd.DB_func import check


logging.basicConfig(level=logging.INFO)


async def timer():
    while True:
        now = datetime.now()
        # next_day = (now +timedelta(day=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        # wait_time=(next_day-now).total_seconds()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        wait_time = (next_minute - now).total_seconds()
        check()
        await asyncio.sleep(wait_time)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(basic_handlers.router, work_handlers.router)
    asyncio.create_task(timer())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
