import aiogram
import keyboards
import states
import utils

from loader import bot


async def create_event_command(message: aiogram.types.Message):
    await message.answer(text='❕Вы находитесь в режиме создания события. '
                              'Для того что бы выйти используйте команду /cancel.')
    await message.answer(text='❔*Как называется ваше событие ?*',
                         parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.get_event_name.set()


async def get_event_name(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_name = message.text
    async with state.proxy() as data:
        data['event_name'] = event_name
    await message.answer(text='❕*Отправьте изображение события, либо нажмите на кнопку \"Без изображения\".*',
                         reply_markup=keyboards.inline.withput_photo_keyboard.without_photo_keyboard(),
                         parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_event_picture(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_picture_id = message.photo[0]["file_id"]
    async with state.proxy() as data:
        data['event_picture_id'] = event_picture_id
    await message.answer(text='❕*Изображение события получено и сохранено, теперь пожалуйста опишите ваше событие.*',
                         parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def without_picture(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['event_picture_id'] = None
    await bot.send_message(chat_id=callback.from_user.id,
                           text='❕*Хорошо, теперь пожалуйста добавьте описание к вашему событию.*',
                           parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_event_description(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_description = message.text
    with utils.database.database as db:
        channels = db.get_channels()
        groups = db.get_groups()
    channel_and_groups, channel_number_to_id = await utils.misc.create_channel_and_group_strings(channels=channels,
                                                                                                 groups=groups)
    async with state.proxy() as data:
        data['event_description'] = event_description
        data['channel_number_to_id'] = channel_number_to_id
    await message.answer(text=f'❕*Выберите через пробел каналы, группы в которые отправить событие.*\n'
                              f'{channel_and_groups}\n',
                         parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def select_channel(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    channels_indexes = message.text.split(' ')
    await message.answer(text='❕*Проверьте всё ли правильно:*',
                         parse_mode='Markdown')
    async with state.proxy() as data:
        event_name = data['event_name']
        event_picture_id = data['event_picture_id']
        event_description = data['event_description']
        data['channels_indexes'] = channels_indexes
    if event_picture_id:
        await message.answer_photo(photo=event_picture_id, caption=f"*{event_name}*\n{event_description}",
                                   parse_mode='Markdown')
    else:
        await message.answer(text=f'*{event_name}*\n{event_description}',
                             reply_markup=keyboards.inline.send_event.send_event_keyboard(),
                             parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def send_event(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        event_name = data['event_name']
        event_picture_id = data['event_picture_id']
        event_description = data['event_description']
        channels_indexes = data['channels_indexes']
        channel_number_to_id = data['channel_number_to_id']
    for number in channels_indexes:
        if event_picture_id:
            await bot.send_photo(chat_id=channel_number_to_id[number], photo=event_picture_id,
                                 caption=f"*{event_name}*\n{event_description}",
                                 parse_mode='Markdown')
        else:
            await bot.send_message(chat_id=channel_number_to_id[number], text=f"*{event_name}*\n{event_description}",
                                   parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text='✅Событие отправлено.')
    await state.finish()


def register_create_event_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=create_event_command, commands=['create_event'])
    dp.register_message_handler(callback=get_event_name, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_event_name)
    dp.register_message_handler(callback=get_event_picture, content_types=['photo'],
                                state=states.create_event_states.CreateEventStates.get_event_picture)
    dp.register_callback_query_handler(callback=without_picture, text='without_picture',
                                       state=states.create_event_states.CreateEventStates.get_event_picture)
    dp.register_message_handler(callback=get_event_description, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_event_description)
    dp.register_message_handler(callback=select_channel, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.select_channel)
    dp.register_callback_query_handler(callback=send_event, text='send_event',
                                       state=states.create_event_states.CreateEventStates.is_all_correct)
