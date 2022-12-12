import aiogram
import states

from loader import bot


async def cancel_buttons(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text='ℹ️*Отправка события / опроса отменена.*',
                           parse_mode='Markdown')
    await state.finish()


def register_cancel_buttons_handlers(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(callback=cancel_buttons, text='cancel',
                                       state=states.create_event_states.CreateEventStates.send_event)
