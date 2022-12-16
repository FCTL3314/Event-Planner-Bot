import time
import logging
import aiogram
import handlers
import utils

from loader import dp
from data.config import LOGGING_LEVEL, LOGGING_FILE_NAME, LOGGING_FILE_MODE, LOGGING_FORMAT


logging.basicConfig(level=LOGGING_LEVEL, filename=f"{LOGGING_FILE_NAME}.log", filemode=LOGGING_FILE_MODE,
                    format=LOGGING_FORMAT)

handlers.commands.cancel_command.register_cancel_command_handlers(dp=dp)
handlers.commands.clear_command.register_clear_command_handler(dp=dp)
handlers.commands.start_command.register_start_command_handler(dp=dp)
handlers.callbacks.vote_buttons.register_vote_buttons_handler(dp=dp)
handlers.callbacks.without_picture.register_without_picture(dp=dp)
handlers.callbacks.without_link_button.register_without_link_button(dp=dp)
handlers.callbacks.cancel_buttons.register_cancel_buttons_handlers(dp=dp)
handlers.messages.bot_channel_actions.register_bot_added_to_channel_handlers(dp=dp)
handlers.commands.create_event_command.register_create_event_command_handlers(dp=dp)
handlers.commands.statistics_command.register_statistics_command(dp=dp)

if __name__ == '__main__':
    while True:
        try:
            aiogram.executor.start_polling(dispatcher=dp, on_startup=utils.on_startup, skip_updates=True)
        except Exception as log_info:
            logging.exception(msg=log_info)
            logging.info(msg='Stopping...')
            time.sleep(15)
            logging.info(msg='Starting...')
