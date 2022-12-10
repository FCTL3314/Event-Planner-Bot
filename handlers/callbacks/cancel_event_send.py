import aiogram
import states

from loader import bot


async def cancel_event_send(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text='ℹ️*Отправка события отменена.*', parse_mode='Markdown')
    await state.finish()


def register_cancel_event_send_handlers(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(callback=cancel_event_send, text='cancel',
                                       state=[states.create_event_states.CreateEventStates.get_event_name,
                                              states.create_event_states.CreateEventStates.get_event_description,
                                              states.create_event_states.CreateEventStates.get_event_picture,
                                              states.create_event_states.CreateEventStates.select_channel,
                                              states.create_event_states.CreateEventStates.send_event])
