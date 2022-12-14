import aiogram
import keyboards


async def send_unable_execute_stop_command_message(message: aiogram.types.Message):
    await message.answer(text="❕Вам нечего отменять.")


async def send_preview_of_event(message: aiogram.types.Message, event_picture_id: str, event_name: str,
                                event_description: str):
    if event_picture_id:
        await message.answer_photo(photo=event_picture_id, caption=f"*{event_name}*\n{event_description}",
                                   reply_markup=keyboards.inline.send_event.send_event_keyboard(),
                                   parse_mode='Markdown')
    else:
        await message.answer(text=f'*{event_name}*\n{event_description}',
                             reply_markup=keyboards.inline.send_event.send_event_keyboard(),
                             parse_mode='Markdown')
