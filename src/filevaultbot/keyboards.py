from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_dynamic_pagination_keyboard(page: int, total_pages: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='◀️ Previous' if page > 1 else ' ',
        callback_data=f'page_{page - 1}' if page > 1 else 'none',
    )
    builder.button(text=f'{page}/{total_pages}', callback_data='current')
    builder.button(
        text='Next ▶️' if page < total_pages else ' ',
        callback_data=f'page_{page + 1}' if page < total_pages else 'none',
    )
    return builder.as_markup()
