import aiogram
import states
import utils

from data.config import BOT_ADMIN_IDS


async def statistics_command(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if message.from_user.id in BOT_ADMIN_IDS:
        with utils.database.database as db:
            events = db.execute(f'SELECT message_id, chat_id, event_name, creation_date '
                                f'FROM events WHERE message_id IN '
                                f'(SELECT message_id FROM (SELECT DISTINCT chat_id, message_id FROM events)) '
                                f'ORDER BY creation_date DESC')
        result = []
        channels_numbers_dict = dict()
        for i, data in enumerate(events, 1):
            with utils.database.database as db:
                channel_tittle = db.execute(f'SELECT channel_name FROM channels WHERE channel_id = {data[1]}')
                group_tittle = db.execute(f'SELECT group_name FROM groups WHERE group_id = {data[1]}')
            if channel_tittle:
                if result and len(result[-1] + f'<b>{i}:\nНазвание мероприятия:\n</b> {data[2]}\n<b>Дата создания:\n'
                                               f'</b> {data[3]}\n<b>Канал:\n</b> {channel_tittle[0][0]}\n') < 4096:
                    result[-1] += f'● <b>{i}\nНазвание мероприятия:\n</b> {data[2]}\n<b>' \
                                  f'Дата создания:\n</b> {data[3]}\n<b>Канал:\n</b> {channel_tittle[0][0]}\n'
                    channels_numbers_dict[i] = data[0], data[1], data[2], data[3]
                else:
                    result.append(f'● <b>{i}\nНазвание мероприятия:\n</b> {data[2]}\n<b>'
                                  f'Дата создания:\n</b> {data[3]}\n<b>Канал:\n</b> {channel_tittle[0][0]}\n')
                    channels_numbers_dict[i] = data[0], data[1], data[2], data[3]
            else:
                if result and len(result[-1] + f'<b>{i}:\nНазвание мероприятия:\n</b> {data[2]}\n<b>Дата создания:\n'
                                               f'</b> {data[3]}\n<b>Группа:\n</b> {group_tittle[0][0]}\n') < 4096:
                    result[-1] += f'● <b>{i}\nНазвание мероприятия:\n</b> {data[2]}\n<b>' \
                                  f'Дата создания:\n</b> {data[3]}\n<b>Группа:\n</b> {group_tittle[0][0]}\n'
                    channels_numbers_dict[i] = data[0], data[1], data[2], data[3]
                else:
                    result.append(f'● <b>{i}\nНазвание мероприятия:\n</b> {data[2]}\n<b>Дата создания:\n</b> '
                                  f'{data[3]}\n<b>Группа:\n</b> {group_tittle[0][0]}\n')
                    channels_numbers_dict[i] = data[0], data[1], data[2], data[3]
        if not result:
            await message.answer(text='*ℹ️У вас нет активных мероприятий.*\n', parse_mode='Markdown')
            await state.finish()
        else:
            async with state.proxy() as data:
                data['channels_numbers_dict'] = channels_numbers_dict
            await states.statistic_command_states.CreateStatisticsStates.get_channels.set()
            await message.answer(text=f'<b> ℹ️Отправьте номер мероприятия по которому нужно отобразить '
                                      f'статистику:</b>', parse_mode='HTML')
            for channels_message in result:
                await message.answer(text=channels_message, parse_mode='HTML')
            await message.answer(text=f'<b> Напишите /cancel что бы отменить выбор мероприятия.</b>', parse_mode="HTML")


async def get_channel_to_show(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    channel_number = message.text
    async with state.proxy() as data:
        channels_numbers_dict = data['channels_numbers_dict']
    if channel_number.replace(' ', '').isdigit() and int(channel_number.replace(' ', '')) in \
            channels_numbers_dict.keys():
        async with state.proxy() as data:
            event_data = data['channels_numbers_dict'][int(channel_number)]
        with utils.database.database as db:
            users_who_vote_fire = db.execute(query=f"SELECT user_id, first_name, last_name FROM user_votes WHERE "
                                                   f"(message_id = {event_data[0]}) and (chat_id = {event_data[1]}) "
                                                   f"and (vote = 'fire')")
            users_who_vote_think = db.execute(query=f"SELECT user_id, first_name, last_name FROM user_votes WHERE "
                                                    f"(message_id = {event_data[0]}) and (chat_id = {event_data[1]}) "
                                                    f"and (vote = 'think')")
        await message.answer(text=f"ℹ️<b>Мероприятие:\n</b> {event_data[2]}\n<b>Дата создания\n</b>: {event_data[3]}",
                             parse_mode='HTML')

        users_fire_votes_text_divided_by_4096_symbols = await utils.misc.create_users_vote_text(
            users=users_who_vote_fire)

        await message.answer(text='*Пользователи которые нажали* 🔥:', parse_mode='Markdown')

        for votes_message in users_fire_votes_text_divided_by_4096_symbols:
            await message.answer(text=votes_message, parse_mode='HTML')

        users_think_votes_text_divided_by_4096_symbols = await utils.misc.create_users_vote_text(
            users=users_who_vote_think)
        await message.answer(text='*Пользователи которые нажали* 🤔:', parse_mode='Markdown')

        for votes_message in users_think_votes_text_divided_by_4096_symbols:
            await message.answer(text=votes_message, parse_mode='HTML')

        await state.finish()
    else:
        await message.answer(text='⚠️*Введённое вами число некорректно. Отправьте номер мероприятия снова.*',
                             parse_mode='Markdown')


def register_statistics_command(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=statistics_command, commands=['statistics'])
    dp.register_message_handler(callback=get_channel_to_show, content_types=['text'],
                                state=states.statistic_command_states.CreateStatisticsStates.get_channels)
