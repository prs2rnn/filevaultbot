from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from database import file_db
from keyboards import get_dynamic_pagination_keyboard


async def handle_pagination(callback: CallbackQuery):
    page = int(callback.data.split('_')[1])
    user_id = callback.from_user.id

    result = await file_db.get_user_files_paginated(user_id)

    files_text = '\n'.join(
        [f'• <code>{f['unique_id']}</code> ({f['type']})' for f in result['files']]
    )

    total_pages = (result['total'] + 19) // 20

    await callback.message.edit_text(
        f'<b>Your files (page {page}/{total_pages}):</b>\n\n'
        f'{files_text}\n\n<i>Total files: {result['total']}</i>',
        reply_markup=get_dynamic_pagination_keyboard(page, total_pages),
    )
    await callback.answer()


async def handle_empty_buttons(callback: CallbackQuery):
    await callback.answer()


def register_user_callbacks(dp: Dispatcher):
    '''Registers all user callback handlers with the dispatcher.'''
    dp.callback_query.register(handle_pagination, F.data.startswith('page_'))
    dp.callback_query.register(
        handle_empty_buttons, (F.data == 'current') | (F.data == 'none')
    )
