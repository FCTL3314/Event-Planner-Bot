import aiogram
import states
import utils


async def statistics_command(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    with utils.database.database as db:
        events = db.execute(query=f'SELECT DISTINCT (message_id), event_name, creation_date FROM'
                                  f' event_data ORDER BY creation_date')
    result = ''
    channels_ids_dict = dict()
    for i, data in enumerate(events, 1):
        result += f'{i}. {data[1]}({data[2]})\n'
        channels_ids_dict[i] = data[0], data[1]
    async with state.proxy() as data:
        data['channels_ids_dict'] = channels_ids_dict
    # result += f'<a href="tg://user?id=761331499">F_C_T_L</a>'
    # with utils.database.database as db:
    #     votes = db.execute(query=f'SELECT DISTINCT (message_id), vote FROM event_votes')
    await states.statistic_command_states.CreateStatisticsStates.get_channels.set()
    await message.answer(text=f'<b> ℹ️Введите номер события по которому нужно отобразить статистику:</b>\n{result}'
                              f'<b> Напишите /cancel что бы отменить выбор события.</b>',
                         parse_mode="HTML")


async def get_channel_to_show(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    channel_number = message.text
    async with state.proxy() as data:
        channels_ids_dict = data['channels_ids_dict']
    if channel_number.replace(' ', '').isdigit() and int(channel_number.replace(' ', '')) in channels_ids_dict.keys():
        async with state.proxy() as data:
            channel = data['channels_ids_dict'][int(channel_number)]
        with utils.database.database as db:
            users_who_vote_like = db.execute(query=f"SELECT user_id FROM event_votes WHERE "
                                                   f"(message_id = {channel[0]}) and (vote = 'like')")
            await message.answer(text=await create_users_who_vote_like_text(users=users_who_vote_like),
                                 parse_mode='HTML')
            await state.finish()
    else:
        await message.answer(text='⚠️*Введённое вами число некорректно.*', parse_mode='Markdown')


async def create_users_who_vote_like_text(users):
    result = '<b>Пользователи которые нажали</b> 👍🏼:\n'
    for i, user_id in enumerate(users, 1):
        result += f'{i}. <a href="tg://user?id={user_id[0]}">F_C_T_L</a>\n'
    return result


def register_statistics_command(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=statistics_command, commands=['statistics'])
    dp.register_message_handler(callback=get_channel_to_show, content_types=['text'],
                                state=states.statistic_command_states.CreateStatisticsStates.get_channels)
