import time
import logging
import aiogram
import handlers
import utils

from loader import dp
from data.config import LOGGING_LEVEL, LOGGING_FILE_NAME, LOGGING_FILE_MODE, LOGGING_FORMAT

logging.basicConfig(level=LOGGING_LEVEL, filename=f"{LOGGING_FILE_NAME}.log", filemode=LOGGING_FILE_MODE,
                    format=LOGGING_FORMAT)

handlers.messages.bot_added_to_channel.register_bot_added_to_channel_handler(dp=dp)
handlers.commands.cancel_command.register_cancel_command_handler(dp=dp)
handlers.commands.create_event_command.register_create_event_command_handler(dp=dp)

if __name__ == '__main__':
    while True:
        try:
            aiogram.executor.start_polling(dispatcher=dp, on_startup=utils.on_startup, skip_updates=True)
        except Exception as log_info:
            logging.exception(msg=log_info)
            time.sleep(5)
