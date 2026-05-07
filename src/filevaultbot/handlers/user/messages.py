from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from state.states import User
from utils import generate_unique_id

# Global dictionary to store file mappings and IDs
# WARNING: This approach is NOT recommended for production as it's not user-isolated
# Structure:
# {
#   'file_mapping': {unique_id: {'original_id': str, 'type': str}},
#   'ids_by_type': {file_type: [unique_ids]}
# }
ids = {}


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

    file_mapping = ids.get('file_mapping', {})
    ids_by_type = ids.get('ids_by_type', {})

    if type not in ids_by_type:
        ids_by_type[type] = []
    if original_id not in (i['original_id'] for i in file_mapping.values()):
        ids_by_type[type].append(unique_id)
        file_mapping[unique_id] = {'original_id': original_id, 'type': type}
        await message.answer(
            f'File proceeded!\n\n<b>Type:</b> {type}\n<b>Your file ID</b>: <code>{unique_id}</code>'
        )
    else:
        await message.answer(
            f'File already exists!\n\n<b>Its ID:</b> <code>{unique_id}</code>'
        )

    ids.update(file_mapping=file_mapping, ids_by_type=ids_by_type)

    print(ids)
    await state.clear()


async def get_file_by_id(message: Message, command: CommandObject):
    """Handler for the /get command — retrieves and sends a previously uploaded file by its unique ID."""
    unique_id = command.args

    if not unique_id:
        return await message.answer('Specify file ID: <code>/get file_id</code>')

    file_mapping = ids.get('file_mapping', {})

    if unique_id not in file_mapping:
        return await message.answer(f'No files found with ID: <code>{unique_id}</code>')

    original_id, type = file_mapping[unique_id].values()

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
