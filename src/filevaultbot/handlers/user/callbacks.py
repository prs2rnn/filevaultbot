import html
import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards import (
    get_number_keyboard,
    get_on_true_keyboard,
    get_play_button,
    get_stop_button,
)
from states.state import User

router_callback = Router()


@router_callback.callback_query(F.data == 'play')
async def play(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f'Bot asked you a number. Chose an integer from 1 to 10, e.g. 10',
        reply_markup=get_number_keyboard(),
    )
    await state.set_state(User.number)
    random_number = random.randint(1, 10)
    await state.update_data(random_number=random_number, user_numbers=[])


@router_callback.callback_query(F.data == 'stop')
async def stop(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text=f'This bot asks you a number from 1 to 10, and you try to guess it',
        reply_markup=get_play_button(),
    )


@router_callback.callback_query(User.number, F.data.startswith('num_'))
async def play(callback: CallbackQuery, state: FSMContext):
    user_number = int(callback.data.split('_')[1])
    data = await state.get_data()
    tries = data.get('user_numbers', [])
    if user_number not in tries:
        tries.append(user_number)
    print(data)
    if user_number == data.get('random_number'):
        await state.clear()
        await callback.message.edit_text(
            text=f'🎉 Well done! You guessed: {user_number}!',
            reply_markup=get_on_true_keyboard(),
        )
    else:
        await callback.message.edit_text(
            text=f'Incorrect! Try again.\nYou chose: {user_number}\nIncorrect: {str(tries).replace('[', '').replace(']', '')}',
            reply_markup=get_number_keyboard(wrong_numbers=tries),
        )
