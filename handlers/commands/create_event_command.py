import aiogram
import states


async def create_event_command(message: aiogram.types.Message):
    await message.answer(text='❕Вы находитесь в режиме создания события. '
                              'Для того что бы выйти используйте команду /cancel.')
    await message.answer(text='❔Как называется ваше событие ?')
    await states.create_event_states.CreateEventStates.get_event_name.set()


async def get_event_name(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_name = message.text
    async with state.proxy() as data:
        data['event_name'] = event_name
    await message.answer(text='❕Хорошо, теперь пожалуйста опишите ваше событие.')
    await states.create_event_states.CreateEventStates.next()


async def get_event_description(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    event_description = message.text
    async with state.proxy() as data:
        data['event_description'] = event_description
    await message.answer(text='✅Событие успешно создано и опубликовано!')
    await state.finish()


def register_create_event_command_handler(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=create_event_command, commands=['create_event'])
    dp.register_message_handler(callback=get_event_name, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_event_name)
    dp.register_message_handler(callback=get_event_description, content_types=['text'],
                                state=states.create_event_states.CreateEventStates.get_event_description)
