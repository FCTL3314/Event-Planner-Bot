import aiogram
import utils

from data.config import BOT_ADMIN_IDS
from loader import bot


async def bot_added_to_channel(message: aiogram.types.Message):
    channel_info = message.chat
    status = message["new_chat_member"]["status"]
    if channel_info['type'] == 'channel':
        if status == 'administrator':
            with utils.database.database as db:
                db.add_channel(channel_name=channel_info['title'], channel_id=channel_info['id'])
            for admin in BOT_ADMIN_IDS:
                await bot.send_message(chat_id=admin, text=f'✅Бот добавлен в канал: [{channel_info["title"]}].')
        elif status == 'kicked' or status == 'left':
            with utils.database.database as db:
                db.remove_channel(channel_id=channel_info['id'])
            for admin in BOT_ADMIN_IDS:
                await bot.send_message(chat_id=admin, text=f'✅Бот удалён из канала: [{channel_info["title"]}].')
    elif channel_info['type'] == 'group':
        if status == 'member':
            with utils.database.database as db:
                db.add_group(group_name=channel_info['title'], group_id=channel_info['id'])
            for admin in BOT_ADMIN_IDS:
                await bot.send_message(chat_id=admin, text=f'✅Бот добавлен в группу: [{channel_info["title"]}].')
        elif status == 'kicked' or status == 'left':
            with utils.database.database as db:
                db.remove_group(group_id=channel_info['id'])
            for admin in BOT_ADMIN_IDS:
                await bot.send_message(chat_id=admin, text=f'✅Бот удалён из группы: [{channel_info["title"]}].')


def register_bot_added_to_channel_handler(dp: aiogram.Dispatcher):
    dp.register_my_chat_member_handler(callback=bot_added_to_channel)
