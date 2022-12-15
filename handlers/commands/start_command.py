import aiogram


async def start_command(message: aiogram.types.Message):
    await message.answer(text='ℹ️<b>Как пользоваться ботом ?</b>\n'
                              '● Первым делом, вам нужно добавить бота в любые ваши группы/каналы, после чего, '
                              'бот отправит вам сообщение о том, что он успешно добавлен.\n'
                              '● После добавления бота, вы можете создавать мероприятия с помощью команды '
                              '/create_event.\n'
                              '● Для просмотра статистики по мероприятиям используется команда /statistics.',
                         parse_mode='HTML')


def register_start_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=start_command, commands=['start'])
