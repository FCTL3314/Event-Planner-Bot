import aiogram
import utils

from loader import bot


async def on_startup(dp: aiogram.Dispatcher):
    await bot.set_my_commands([
        aiogram.types.BotCommand('create_event', 'Создать событие.'),
    ])
    with utils.database.database as db:
        db.create_tables()
