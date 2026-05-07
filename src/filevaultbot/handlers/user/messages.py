from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from state.states import User

ids = {}


async def start(message: Message, state: FSMContext):
    await message.answer(
        text=f'<b>Welcome to the bot!</b>\nSend me a file, and I\'ll return its ID',
    )
    await state.set_state(User.file)


async def file(message: Message, state: FSMContext):
    if message.document:
        type, id = 'document', message.document.file_id
    elif message.photo:
        type, id = 'photo', message.photo[-1].file_id
    elif message.video:
        type, id = 'video', message.video.file_id
    elif message.audio:
        type, id = 'audio', message.audio.file_id
    elif message.voice:
        type, id = 'voice', message.voice.file_id
    else:
        type, id = 'na', 'N/A'

    if type not in ids.keys():
        ids[type] = []
    if id not in ids[type]:
        ids[type].append(id)
        await message.answer(f'File proceeded!\n\nYour file ID: <code>{id}</code>')
    else:
        await message.answer(f'File already exists!\n\nIts ID: <code>{id}</code>')

    print(ids)
    await state.clear()


async def get_file_by_id(message: Message, command: CommandObject):
    id = command.args
    for type, values in ids.items():
        for v in values:
            if v == id:
                if type == 'document':
                    return await message.answer_document(id)
                elif type == 'photo':
                    return await message.answer_photo(id)
                elif type == 'video':
                    return await message.answer_video(id)
                elif type == 'audio':
                    return await message.answer_audio(id)
                elif type == 'voice':
                    return await message.answer_voice(id)
    await message.answer(text=f'No files found with ID: {id}')
    print(id)


def register_user_messages(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(
        file,
        StateFilter(User.file),
        F.document | F.photo | F.video | F.audio | F.voice,
    )
    dp.message.register(
        get_file_by_id,
        Command('get'),
    )
