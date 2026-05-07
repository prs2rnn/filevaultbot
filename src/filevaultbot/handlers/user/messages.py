from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import file_db
from state.states import User
from utils import generate_unique_id


async def start(message: Message, state: FSMContext):
    """Handler for the /start command."""
    await message.answer(
        text=f'<b>Welcome to the bot!</b>\nSend me a file, and I\'ll return its ID',
    )
    await state.set_state(User.file)


async def file(message: Message, state: FSMContext):
    """Handler for file uploads (documents, photos, videos, audio, voice messages)."""
    if message.document:
        type, original_id = 'document', message.document.file_id
    elif message.photo:
        type, original_id = 'photo', message.photo[-1].file_id
    elif message.video:
        type, original_id = 'video', message.video.file_id
    elif message.audio:
        type, original_id = 'audio', message.audio.file_id
    elif message.voice:
        type, original_id = 'voice', message.voice.file_id
    else:
        type, original_id = 'na', 'N/A'

    if not original_id or original_id == 'N/A':
        return await message.answer("Failed to get ID of the file")

    unique_id = generate_unique_id()

    # save
    success = await file_db.add_file(unique_id, original_id, type, message.from_user.id)

    if success:
        await message.answer(
            f'File proceeded!\n\n<b>Type:</b> {type}\n<b>Your file ID</b>: <code>{unique_id}</code>'
        )
    else:
        await message.answer(f'File already exists!')

    await state.clear()


async def get_file_by_id(message: Message, command: CommandObject):
    """Handler for the /get command — retrieves and sends a previously uploaded file by its unique ID."""
    unique_id = command.args

    if not unique_id:
        return await message.answer('Specify file ID: <code>/get file_id</code>')

    file_info = await file_db.get_file_by_unique_id(unique_id)

    if not file_info:
        return await message.answer(f'No files found with ID: <code>{unique_id}</code>')

    original_id, type = file_info['original_id'], file_info['type']

    type_methods = {
        'document': message.answer_document,
        'photo': message.answer_photo,
        'video': message.answer_video,
        'audio': message.answer_audio,
        'voice': message.answer_voice,
    }

    try:
        await type_methods[type](original_id)
    except Exception as e:
        await message.answer(f'Error occurred, when sending file: {e}')


async def get_user_files(message: Message):
    user_id = message.from_user.id
    user_files = await file_db.get_user_files(user_id)
    pretty = ''.join(
        [f'• {raw['type']} <code>{raw['unique_id']}</code>\n' for raw in user_files]
    )
    await message.answer(f'<b>All Entries</b> ({user_id})\n\n{pretty}')


def register_user_messages(dp: Dispatcher):
    """Registers all user message handlers with the dispatcher."""
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
    dp.message.register(get_user_files, Command('all'))
