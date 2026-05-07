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

    if not id or id == 'N/A':
        return await message.answer("Failed to get ID of the file")

    if type not in ids.keys():
        ids[type] = []
    if id not in ids[type]:
        ids[type].append(id)
        await message.answer(
            f'File proceeded!\n\n<b>Type:</b> {type}\n<b>Your file ID</b>: <code>{id}</code>'
        )
    else:
        await message.answer(
            f'File already exists!\n\n<b>Its ID:</b> <code>{id}</code>'
        )

    print(ids)
    await state.clear()


async def get_file_by_id(message: Message, command: CommandObject):
    id = command.args
    if not id:
        return await message.answer('Specify file ID: <code>/get file_id</code>')

    type_methods = {
        'document': message.answer_document,
        'photo': message.answer_photo,
        'video': message.answer_video,
        'audio': message.answer_audio,
        'voice': message.answer_voice,
    }

    for type, values in ids.items():
        if id in values and type in type_methods:
            try:
                return await type_methods[type](id)
            except Exception as e:
                return await message.answer(f'Error occurred, when sending file: {e}')

    await message.answer(f'No files found with ID: <code>{id}</code>')


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
