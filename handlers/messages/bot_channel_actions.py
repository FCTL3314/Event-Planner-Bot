import aiogram
import utils

from data.config import BOT_ADMIN_IDS
from loader import bot


async def bot_channel_actions(message: aiogram.types.Message):
    if message["from"]["id"] in BOT_ADMIN_IDS:
        channel_info = message.chat
        status = message["new_chat_member"]["status"]
        if channel_info['type'] == 'channel':
            if status == 'administrator':
                with utils.database.database as db:
                    db.execute(f"INSERT INTO channels VALUES ({channel_info['id']}, '{channel_info['title']}')")
                for admin in BOT_ADMIN_IDS:
                    await bot.send_message(chat_id=admin, text=f'ℹ️Бот добавлен в канал: {channel_info["title"]}.')
            elif status == 'kicked' or status == 'left':
                await utils.misc.delete_all_chat_info(chat_id=channel_info['id'])
                for admin in BOT_ADMIN_IDS:
                    await bot.send_message(chat_id=admin, text=f'ℹ️Бот удалён из канала: {channel_info["title"]}.')
        elif channel_info['type'] == 'group':
            if status == 'member':
                with utils.database.database as db:
                    db.execute(f"INSERT INTO groups VALUES ({channel_info['id']}, '{channel_info['title']}')")
                for admin in BOT_ADMIN_IDS:
                    await bot.send_message(chat_id=admin, text=f'ℹ️Бот добавлен в группу: {channel_info["title"]}.')
            elif status == 'kicked' or status == 'left':
                await utils.misc.delete_all_chat_info(chat_id=channel_info['id'])
                for admin in BOT_ADMIN_IDS:
                    await bot.send_message(chat_id=admin, text=f'ℹ️Бот удалён из группы: {channel_info["title"]}.')


def register_bot_added_to_channel_handlers(dp: aiogram.Dispatcher):
    dp.register_my_chat_member_handler(callback=bot_channel_actions)
