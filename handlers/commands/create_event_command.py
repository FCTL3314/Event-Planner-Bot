import aiogram
import filters
import keyboards
import states
import utils

from loader import bot


async def create_event_command(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    with utils.database.database as db:
        channels = db.get_channels()
        groups = db.get_groups()
    channels_text = await utils.misc.create_channels_text(channels=channels, groups=groups)
    channels_ids_dict = await utils.misc.get_channels_indexes(channels=channels, groups=groups)
    async with state.proxy() as data:
        data['channels_text'] = channels_text
        data['channels_ids_dict'] = channels_ids_dict
    await message.answer(text='ℹВы находитесь в режиме создания события. '
                              'Для того что бы выйти используйте команду /cancel.')
    await message.answer(text='❕*Отправьте название события.*',
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
    await message.answer(text='✅*Изображение события получено и сохранено.\n❕Отправьте описание события.*',
                         parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def without_picture(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['event_picture_id'] = None
    await bot.send_message(chat_id=callback.from_user.id, text='❕*Отправьте описание события.*',
                           parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_event_description(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_description = message.text
    async with state.proxy() as data:
        data['event_description'] = event_description
        channels_text = data['channels_text']
    await message.answer(text=f'❕*Выберите номер канала, либо укажите через пробел номера каналов, '
                              f'в которые необходимо отправить событие.*\n{channels_text}', parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_channels_to_send(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        channels_ids_dict = data['channels_ids_dict']
    if await filters.is_text_consists_of_digits.is_text_consists_of_digits(
            text=message.text) and await filters.is_channel_numbers_correct.is_channel_numbers_correct(
            text=message.text, channels_ids_dict=channels_ids_dict):
        channels_indexes = message.text.split(' ')
        await message.answer(text='❕*Проверьте правильность оформления:*', parse_mode='Markdown')
        async with state.proxy() as data:
            event_name = data['event_name']
            event_picture_id = data['event_picture_id']
            event_description = data['event_description']
            data['channels_indexes'] = channels_indexes
        await utils.misc.send_message.send_preview_of_event_post(message=message, event_name=event_name,
                                                                 event_picture_id=event_picture_id,
                                                                 event_description=event_description)
        await states.create_event_states.CreateEventStates.next()
    else:
        await message.answer(text='❗*Проверьте правильность сообщения.*', parse_mode='Markdown')


async def send_event(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        event_name = data['event_name']
        event_picture_id = data['event_picture_id']
        event_description = data['event_description']
        channels_indexes = data['channels_indexes']
        channels_ids_dict = data['channels_ids_dict']
    for number in channels_indexes:
        if event_picture_id:
            await bot.send_photo(chat_id=channels_ids_dict[number], photo=event_picture_id,
                                 caption=f"*{event_name}*\n{event_description}",
                                 reply_markup=keyboards.inline.plus_and_minus_counter_keyboard.plus_and_minus_counter_keyboard(),
                                 parse_mode='Markdown')
        else:
            await bot.send_message(chat_id=channels_ids_dict[number], text=f"*{event_name}*\n{event_description}",
                                   reply_markup=keyboards.inline.plus_and_minus_counter_keyboard.plus_and_minus_counter_keyboard(),
                                   parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text='✅Событие успешно отправлено.')
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
    dp.register_message_handler(callback=get_channels_to_send, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.select_channel)
    dp.register_callback_query_handler(callback=send_event, text='send_event',
                                       state=states.create_event_states.CreateEventStates.is_all_correct)
