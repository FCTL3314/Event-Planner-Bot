import aiogram
import states

from loader import bot


async def without_picture(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['link_button_name'] = None
        data['link_button_url'] = None
        channels_text = data['channels_text']
    await bot.send_message(chat_id=callback.message.chat.id,
                           text=f'❕*Отправьте номер канала, либо укажите через пробел номера каналов, '
                                f'в которые необходимо отправить событие:*\n{channels_text}', parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


def register_without_link_button(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(callback=without_picture, text='without_link_button',
                                       state=states.create_event_states.CreateEventStates.get_link_button_name_and_url)
