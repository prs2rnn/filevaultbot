import html

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import get_play_button
from states.state import User

router_message = Router()


@router_message.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        text=f'<b>Hello, {html.escape(message.from_user.first_name)}!</b>\nThis bot asks you a number from 1 to 10, and you try to guess it',
        reply_markup=get_play_button(),
    )
