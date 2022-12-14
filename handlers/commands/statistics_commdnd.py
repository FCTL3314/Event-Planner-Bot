import aiogram
import states
import utils


async def statistics_command(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    with utils.database.database as db:
        events = db.execute(f'SELECT message_id, chat_id, event_name, creation_date '
                            f'FROM event_data WHERE message_id IN '
                            f'(SELECT message_id FROM (SELECT DISTINCT chat_id, message_id FROM event_data))')
    result = ''
    channels_numbers_dict = dict()
    for i, data in enumerate(events, 1):
        result += f'{i}. {data[2]}({data[3]})\n'
        channels_numbers_dict[i] = data[0], data[1], data[3]
    async with state.proxy() as data:
        data['channels_numbers_dict'] = channels_numbers_dict
    await states.statistic_command_states.CreateStatisticsStates.get_channels.set()
    await message.answer(text=f'<b> ℹ️Введите номер события по которому нужно отобразить статистику:</b>\n{result}'
                              f'<b> Напишите /cancel что бы отменить выбор события.</b>',
                         parse_mode="HTML")


async def get_channel_to_show(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    channel_number = message.text
    async with state.proxy() as data:
        channels_numbers_dict = data['channels_numbers_dict']
    if channel_number.replace(' ', '').isdigit() and int(channel_number.replace(' ', '')) in \
            channels_numbers_dict.keys():
        async with state.proxy() as data:
            event_data = data['channels_numbers_dict'][int(channel_number)]
        with utils.database.database as db:
            users_who_vote_fire = db.execute(query=f"SELECT user_id, first_name, last_name FROM event_votes WHERE "
                                                   f"(message_id = {event_data[0]}) and (chat_id = {event_data[1]}) "
                                                   f"and (vote = 'fire')")
            users_who_vote_think = db.execute(query=f"SELECT user_id, first_name, last_name FROM event_votes WHERE "
                                                    f"(message_id = {event_data[0]}) and (chat_id = {event_data[1]}) "
                                                    f"and (vote = 'think')")
            await message.answer(text=await create_users_vote_text(users=users_who_vote_fire, emoji='🔥'),
                                 parse_mode='HTML')
            await message.answer(text=await create_users_vote_text(users=users_who_vote_think, emoji='🤔'),
                                 parse_mode='HTML')
            await state.finish()
    else:
        await message.answer(text='⚠️*Введённое вами число некорректно.*', parse_mode='Markdown')


async def create_users_vote_text(users, emoji):
    result = f'<b>Пользователи которые нажали</b> {emoji}:\n'
    for i, data in enumerate(users, 1):
        result += f'{i}. <a href="tg://user?id={data[0]}">{data[1]} {data[2]}</a>\n'
    return result


def register_statistics_command(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=statistics_command, commands=['statistics'])
    dp.register_message_handler(callback=get_channel_to_show, content_types=['text'],
                                state=states.statistic_command_states.CreateStatisticsStates.get_channels)
