import aiogram
import filters
import states
import utils

from loader import bot
from data.config import BOT_ADMIN_IDS


async def create_survey_command(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if message.from_user.id in BOT_ADMIN_IDS:
        with utils.database.database as db:
            channels = db.get_channels()
            groups = db.get_groups()
        if channels or groups:
            channels_text = await utils.misc.create_channels_text(channels=channels, groups=groups)
            channels_ids_dict = await utils.misc.get_channels_indexes(channels=channels, groups=groups)
            async with state.proxy() as data:
                data['channels_text'] = channels_text
                data['channels_ids_dict'] = channels_ids_dict
            await message.answer(text='ℹВы находитесь в режиме создания опроса. '
                                      'Для того что бы выйти используйте команду /cancel.')
            await message.answer(text='❕*Отправьте название опроса.*', parse_mode='Markdown')
            await states.create_survey_states.CreateSurveyStates.get_survey_name.set()
        else:
            await message.answer(text='⚠️Для начала добавьте бота в канал.')


async def get_survey_name(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    survey_name = message.text
    async with state.proxy() as data:
        data['survey_name'] = survey_name
    await message.answer(text='❕*Отправьте варианты опроса разделяя их знаком \'@\'.*\n*Пример:*\n'
                              'Да, конечно я приду!@Нет, у меня не получиться.',
                         parse_mode='Markdown')
    await states.create_survey_states.CreateSurveyStates.next()


async def get_survey_answers(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    if filters.is_survey_answers_correct.is_survey_answers_correct(text=message.text):
        survey_answers = message.text
        async with state.proxy() as data:
            data['survey_answers'] = survey_answers
            channels_text = data['channels_text']
        await message.answer(text=f'❕*Отправьте номер канала, либо укажите через пробел номера каналов, '
                                  f'в которые необходимо отправить опрос:*\n{channels_text}', parse_mode='Markdown')
        await states.create_survey_states.CreateSurveyStates.next()
    else:
        await message.answer(text='⚠️Варианты вопроса отправлены в неверной форме.')


async def get_channels_to_send(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        channels_ids_dict = data['channels_ids_dict']
    if await filters.is_text_consists_of_digits.is_text_consists_of_digits(
            text=message.text) and await filters.is_channel_numbers_correct.is_channel_numbers_correct(
            text=message.text, channels_ids_dict=channels_ids_dict):
        channels_indexes = message.text.split(' ')
        await message.answer(text='✉️*Предпросмотр:*', parse_mode='Markdown')
        async with state.proxy() as data:
            survey_name = data['survey_name']
            survey_answers = data['survey_answers']
            data['channels_indexes'] = channels_indexes
        await utils.misc.send_message.send_preview_of_survey(message=message, survey_name=survey_name,
                                                             survey_answers=survey_answers)
        await states.create_survey_states.CreateSurveyStates.next()
    else:
        await message.answer(text='⚠️*Введённые вами номера групп не корректны, попробуйте снова.*',
                             parse_mode='Markdown')


async def send_survey(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        survey_name = data['survey_name']
        survey_answers = data['survey_answers']
        channels_indexes = data['channels_indexes']
        channels_ids_dict = data['channels_ids_dict']
    for number in channels_indexes:
        await bot.send_poll(chat_id=channels_ids_dict[number], question=survey_name, is_anonymous=False,
                            options=survey_answers.split('@'))
    await bot.send_message(chat_id=callback.from_user.id, text='✅Опрос успешно отправлен!')
    await state.finish()


def register_create_survey_command_handlers(dp: aiogram.Dispatcher):
    dp.register_message_handler(callback=create_survey_command, commands=['create_survey'])
    dp.register_message_handler(callback=get_survey_name, content_types=['text'],
                                state=states.create_survey_states.CreateSurveyStates.get_survey_name)
    dp.register_message_handler(callback=get_survey_answers, content_types=['text'],
                                state=states.create_survey_states.CreateSurveyStates.get_survey_answers)
    dp.register_message_handler(callback=get_channels_to_send, content_types=['text'],
                                state=states.create_survey_states.CreateSurveyStates.get_channels_to_send)
    dp.register_callback_query_handler(callback=send_survey, text='send_survey',
                                       state=states.create_survey_states.CreateSurveyStates.send_survey)
