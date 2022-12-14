import aiogram
import filters
import keyboards
import states
import utils
import validators

from data.config import BOT_ADMIN_IDS
from loader import bot


async def create_event_command(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if message.from_user.id in BOT_ADMIN_IDS:
        with utils.database.database as db:
            channels = db.get_channels()
            groups = db.get_groups()
        if channels or groups:
            channels_text = await utils.misc.create_channels_text(channels=channels, groups=groups)
            channels_ids_dict = await utils.misc.get_channels_indexes(channels=channels, groups=groups)
            async with state.proxy() as data:
                data['channels_text'] = channels_text
                data['channels_ids_dict'] = channels_ids_dict
            await message.answer(text='ℹВы находитесь в режиме создания мероприятия. '
                                      'Для того что бы отменить создание, используйте команду /cancel.')
            await message.answer(text='❕*Отправьте название мероприятия.*', parse_mode='Markdown')
            await states.create_event_states.CreateEventStates.get_event_name.set()
        else:
            await message.answer(text='⚠️*Для того, что бы создать мероприятие, бот должен быть хотя бы в '
                                      'одном канале.*', parse_mode='Markdown')


async def get_event_name(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_name = message.text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
    async with state.proxy() as data:
        data['event_name'] = event_name
    await message.answer(text='❕*Отправьте сжатое изображение мероприятия, либо нажмите на кнопку \"Без изображения\".*',
                         reply_markup=keyboards.inline.without_photo.without_photo_keyboard(), parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_event_picture(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_picture_id = message.photo[0]["file_id"]
    async with state.proxy() as data:
        data['event_picture_id'] = event_picture_id
    await message.answer(text='✅*Изображение мероприятия получено и сохранено.\n*', parse_mode='Markdown')
    await message.answer(text='❕*Отправьте описание мероприятия.*', parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_event_description(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_description = message.text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
    async with state.proxy() as data:
        data['event_description'] = event_description
    await message.answer(text=f'❕*Отправьте лимит для кнопки 🔥.*', parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_vote_limit(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    vote_limit = message.text.replace(' ', '')
    if vote_limit.isdigit():
        async with state.proxy() as data:
            data['vote_limit'] = vote_limit
        await message.answer(text=f'❕*Отправьте название кнопки-ссылки, либо нажмите на кнопку \"Без кнопки-ссылки\"*',
                             parse_mode='Markdown',
                             reply_markup=keyboards.inline.withput_link_button.without_photo_keyboard(),
                             disable_web_page_preview=True)
        await states.create_event_states.CreateEventStates.next()
    else:
        await message.answer(text='⚠️*Лимит должен быть числом. Отправьте лимит снова.*', parse_mode='Markdown')


async def get_link_button_name(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    link_button_name = message.text
    async with state.proxy() as data:
        data['link_button_name'] = link_button_name
    await message.answer(text=f'❕*Отправьте ссылку для кнопки \"{link_button_name}\"*', parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


async def get_link_button_url(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    text = message.text
    if validators.url(text):
        async with state.proxy() as data:
            data['link_button_url'] = text
            channels_text = data['channels_text']
        await message.answer(text=f'❕*Отправьте номер канала, либо укажите через пробел номера каналов, '
                                  f'в которые необходимо отправить событие:*\n{channels_text}', parse_mode='Markdown')
        await states.create_event_states.CreateEventStates.next()
    else:
        await message.answer(text='⚠️*Ссылка некорректна. Отправьте ссылку заново.*', parse_mode='Markdown')


async def get_channels_to_send(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        channels_ids_dict = data['channels_ids_dict']
    if await filters.is_text_consists_of_digits.is_text_consists_of_digits(
            text=message.text) and await filters.is_channel_numbers_correct.is_channel_numbers_correct(
            text=message.text, channels_ids_dict=channels_ids_dict):
        channels_indexes = message.text.split(' ')
        await message.answer(text='✉️*Предпросмотр:*', parse_mode='Markdown')
        async with state.proxy() as data:
            event_name = data['event_name']
            event_picture_id = data['event_picture_id']
            event_description = data['event_description']
            data['channels_indexes'] = channels_indexes
        await utils.misc.send_message.send_preview_of_event(message=message, event_name=event_name,
                                                            event_picture_id=event_picture_id,
                                                            event_description=event_description)
        await states.create_event_states.CreateEventStates.next()
    else:
        await message.answer(text='⚠️*Введённые вами номера групп некорректны. Отправьте номера групп заново.*',
                             parse_mode='Markdown')


async def send_event(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        event_name = data['event_name']
        event_picture_id = data['event_picture_id']
        event_description = data['event_description']
        vote_limit = int(data['vote_limit'])
        channels_indexes = data['channels_indexes']
        channels_ids_dict = data['channels_ids_dict']
        link_button_name = data['link_button_name']
        link_button_url = data['link_button_url']
    for number in channels_indexes:
        if event_picture_id:
            first_message = await bot.send_photo(chat_id=channels_ids_dict[number], photo=event_picture_id,
                                                 caption=f"*{event_name}*\n{event_description}",
                                                 reply_markup=keyboards.inline.vote.vote_keyboard(
                                                     fire_button_count=0,
                                                     think_button_count=0,
                                                     link_button_name=link_button_name,
                                                     link_button_url=link_button_url),
                                                 parse_mode='Markdown')
            first_message_id = first_message.message_id
            first_message_chat_id = first_message.chat.id
            await utils.misc.insert_event_into_db(chat_id=first_message_chat_id, message_id=first_message_id,
                                                  event_name=event_name, vote_limit=vote_limit,
                                                  link_button_url=link_button_url, link_button_name=link_button_name)
        else:
            second_message = await bot.send_message(chat_id=channels_ids_dict[number],
                                                    text=f"*{event_name}*\n{event_description}",
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=0,
                                                        think_button_count=0,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url),
                                                    parse_mode='Markdown')
            second_message_id = second_message.message_id
            second_message_chat_id = second_message.chat.id
            await utils.misc.insert_event_into_db(chat_id=second_message_chat_id, message_id=second_message_id,
                                                  event_name=event_name, vote_limit=vote_limit,
                                                  link_button_url=link_button_url, link_button_name=link_button_name)
    await bot.send_message(chat_id=callback.from_user.id, text='✅Событие успешно отправлено!')
    await state.finish()


def register_create_event_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=create_event_command, commands=['create_event'])
    dp.register_message_handler(callback=get_event_name, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_event_name)
    dp.register_message_handler(callback=get_event_picture, content_types=['photo'],
                                state=states.create_event_states.CreateEventStates.get_event_picture)
    dp.register_message_handler(callback=get_event_description, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_event_description)
    dp.register_message_handler(callback=get_vote_limit, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_vote_limit)
    dp.register_message_handler(callback=get_link_button_name, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_link_button_name)
    dp.register_message_handler(callback=get_link_button_url, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_link_button_url)
    dp.register_message_handler(callback=get_channels_to_send, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_channels_to_send)
    dp.register_callback_query_handler(callback=send_event, text='send_event',
                                       state=states.create_event_states.CreateEventStates.send_event)
