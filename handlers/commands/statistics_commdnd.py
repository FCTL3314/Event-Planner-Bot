import aiogram
import utils

from loader import bot


async def statistics_command(message: aiogram.types.Message):
    with utils.database.database as db:
        print(db.execute(query=f'SELECT DISTINCT (message_id) FROM event_votes'))


def register_statistics_command(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=statistics_command, commands=['statistics'])
