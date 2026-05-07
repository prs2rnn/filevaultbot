import logging
import uuid
from logging.handlers import RotatingFileHandler


def generate_unique_id() -> str:
    return str(uuid.uuid4())[:8]


def setup_logging():
    # root
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # clear from existing handlers
    logger.handlers.clear()

    # formatter for all handlers
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # 1. File handler for main logs
    file_handler = RotatingFileHandler(
        'files.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB per file
        backupCount=5,  # Save 5 old files
        encoding='utf-8',
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # INFO - prod, DEBUG - dev

    # 2. console_handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)  # WARNING - prod, DEBUG - dev

    # add to root
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # reduce noise from outer libraries, change WARNING in prod
    logging.getLogger('aiogram').setLevel(logging.DEBUG)
    logging.getLogger('aiosqlite').setLevel(logging.DEBUG)
