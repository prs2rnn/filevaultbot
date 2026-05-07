import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers.user.callbacks import router_callback
from handlers.user.messages import router_message


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    dp = Dispatcher()
    dp.include_routers(router_message, router_callback)
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
