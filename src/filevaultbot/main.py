import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import BOT_TOKEN
from handlers.user.callbacks import register_user_callbacks
from handlers.user.messages import register_user_messages
from utils import setup_logging


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Show welcome message'),
        BotCommand(command='get', description='Retrieve file by ID'),
        BotCommand(command='list', description='View your files'),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        dp = Dispatcher()
        register_user_messages(dp)
        register_user_callbacks(dp)

        bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
        await set_bot_commands(bot)
        logger.info('Bot instance created and commands set')

        logger.info('Starting polling...')
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f'Critical error: {e}', exc_info=True)
    finally:
        await bot.session.close()
        logger.info('Bot stopped gracefully')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped manually!')
