import aiogram
import states
import utils


async def clear_command_states(message: aiogram.types.Message):
    await message.answer(text=f'❗️*Внимание! Данная команда удалит все мероприятия. '
                              f'Для подтверждения введите следующее число:*\n{message.from_user.id}\n'
                              f'*Используйте команду /cancel для отмены.*',
                         parse_mode='Markdown')
    await states.clear_command_states.ClearCommandStates.are_you_sure.set()


async def clear_event_tables(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if message.text == str(message.from_user.id):
        with utils.database.database as db:
            db.execute(f'DROP TABLE events')
            db.execute(f'DROP TABLE user_votes')
            db.create_tables()
        await message.answer(text='✅ Все мероприятия удалены.', parse_mode='Markdown')
        await state.finish()
    else:
        await message.answer(text='⚠️*Введённое вами число неверно. '
                                  'Отправьте его снова или напишите /cancel для отмены.*', parse_mode='Markdown')


def register_clear_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=clear_command_states, commands=['clear'])
    dp.register_message_handler(callback=clear_event_tables, content_types=['text'],
                                state=states.clear_command_states.ClearCommandStates.are_you_sure)
