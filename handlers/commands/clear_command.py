import random
import aiogram
import states
import utils

from data.config import BOT_ADMIN_IDS


async def clear_command_states(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if message.from_user.id in BOT_ADMIN_IDS:
        code = ''
        for i in range(10):
            code += str(random.randint(0, 9))
        async with state.proxy() as data:
            data['code'] = code
        await message.answer(text=f'❗️*Внимание! Данная команда удалит все мероприятия. '
                                  f'Для подтверждения введите следующее число:*\n{code}\n'
                                  f'*Используйте команду /cancel для отмены.*',
                             parse_mode='Markdown')
        await states.clear_command_states.ClearCommandStates.are_you_sure.set()


async def clear_event_tables(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        code = data['code']
    if message.text == code:
        with utils.database.database as db:
            db.execute(f'DROP TABLE events')
            db.execute(f'DROP TABLE user_votes')
            db.create_tables()
        await message.answer(text='✅ *Все мероприятия удалены.*', parse_mode='Markdown')
        await state.finish()
    else:
        await message.answer(text='⚠️*Введённое вами число неверно. '
                                  'Отправьте его снова или напишите /cancel для отмены.*', parse_mode='Markdown')


def register_clear_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=clear_command_states, commands=['clear'])
    dp.register_message_handler(callback=clear_event_tables, content_types=['text'],
                                state=states.clear_command_states.ClearCommandStates.are_you_sure)
