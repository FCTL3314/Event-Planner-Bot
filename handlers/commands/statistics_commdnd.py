import aiogram


async def statistics_command(message: aiogram.types.Message):
    pass


def register_statistics_command(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=statistics_command, commands=['statistics'])
