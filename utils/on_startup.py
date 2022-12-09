import aiogram
import utils

from loader import bot


async def on_startup(dp: aiogram.Dispatcher):
    await bot.set_my_commands([
        aiogram.types.BotCommand('start', 'Начальная информация.'),
        aiogram.types.BotCommand('create_event', 'Создать мероприятие / событие.'),
    ])
    with utils.database.database as db:
        db.create_tables()
