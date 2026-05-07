import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers.user.messages import register_user_messages


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    dp = Dispatcher()
    register_user_messages(dp)
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
