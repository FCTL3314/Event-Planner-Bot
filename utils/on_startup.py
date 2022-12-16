import aiogram
import utils

from loader import bot


async def on_startup(dp: aiogram.Dispatcher):
    await bot.set_my_commands([
        aiogram.types.BotCommand('start', 'Начальная информация.'),
        aiogram.types.BotCommand('create_event', 'Создать событие.'),
        aiogram.types.BotCommand('statistics', 'Посмотреть статистику событий.'),
        aiogram.types.BotCommand('cancel', 'Отменить создание события, опроса.'),
        aiogram.types.BotCommand('clear', 'Удалить все мероприятия.'),
    ])
    with utils.database.database as db:
        db.create_tables()
