import aiogram
import keyboards

from loader import bot


async def vote_buttons(callback: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    vote = callback.data.split(' ')[0]
    amount_of_likes = int(callback.data.split(' ')[1])
    amount_of_dislikes = int(callback.data.split(' ')[2])
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    if vote == 'like':
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes + 1,
                                                amount_of_dislikes=amount_of_dislikes))
    else:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes,
                                                amount_of_dislikes=amount_of_dislikes + 1))


def register_vote_buttons_handler(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(vote_buttons, aiogram.filters.Regexp(regexp='^like|^dislike'))
