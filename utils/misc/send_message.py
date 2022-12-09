import aiogram


async def send_unable_execute_stop_command_message(message: aiogram.types.Message):
    await message.answer(text="❕Вы не создаёте событие.")
