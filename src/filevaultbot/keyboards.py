from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_play_button():
    builder = InlineKeyboardBuilder()
    builder.button(text='Play', callback_data='play')
    return builder.as_markup()


def get_stop_button():
    builder = InlineKeyboardBuilder()
    builder.button(text='Stop', callback_data='stop')
    return builder.as_markup()


def get_on_true_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Play', callback_data='play')
    builder.button(text='Menu', callback_data='stop')
    builder.adjust(2)
    return builder.as_markup()


def get_number_keyboard(wrong_numbers=None):
    if not wrong_numbers:
        wrong_numbers = []
    builder = InlineKeyboardBuilder()
    for i in range(1, 11):
        if i in wrong_numbers:
            text = f'{i} ❌'
        else:
            text = str(i)
        builder.button(text=text, callback_data=f'num_{i}')
    builder.button(text='Stop', callback_data='stop')
    builder.adjust(5, 5, 1)
    return builder.as_markup()
