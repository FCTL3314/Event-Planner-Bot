import aiogram
import states

from loader import bot


async def without_picture(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['event_picture_id'] = None
    await bot.send_message(chat_id=callback.from_user.id, text='❕*Отправьте описание события.*', parse_mode='Markdown')
    await states.create_event_states.CreateEventStates.next()


def register_without_picture(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(callback=without_picture, text='without_picture',
                                       state=states.create_event_states.CreateEventStates.get_event_picture)
