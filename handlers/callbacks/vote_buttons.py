import aiogram
import keyboards
import utils

from loader import bot


async def vote_buttons(callback: aiogram.types.CallbackQuery):
    vote = callback.data.split(' ')[0]
    amount_of_likes = int(callback.data.split(' ')[1])
    amount_of_dislikes = int(callback.data.split(' ')[2])
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    with utils.database.database as db:
        user_vote = db.get_vote(message_id=message_id, user_id=user_id)
    if vote == 'like' and not user_vote:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes + 1,
                                                amount_of_dislikes=amount_of_dislikes))
        with utils.database.database as db:
            db.add_vote(user_id=user_id, message_id=message_id, vote='like')
    elif vote == 'like' and user_vote[0] == 'like':
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes - 1,
                                                amount_of_dislikes=amount_of_dislikes))
        with utils.database.database as db:
            db.remove_vote(user_id=user_id, message_id=message_id)
    elif vote == 'dislike' and not user_vote:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes,
                                                amount_of_dislikes=amount_of_dislikes + 1))
        with utils.database.database as db:
            db.add_vote(user_id=user_id, message_id=message_id, vote='dislike')
    elif vote == 'dislike' and user_vote[0] == 'dislike':
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes,
                                                amount_of_dislikes=amount_of_dislikes - 1))
        with utils.database.database as db:
            db.remove_vote(user_id=user_id, message_id=message_id)
    elif vote == 'like' and user_vote[0] == 'dislike':
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes + 1,
                                                amount_of_dislikes=amount_of_dislikes - 1))
        with utils.database.database as db:
            db.remove_vote(user_id=user_id, message_id=message_id)
            db.add_vote(user_id=user_id, message_id=message_id, vote='like')
    elif vote == 'dislike' and user_vote[0] == 'like':
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote.vote_keyboard(
                                                amount_of_likes=amount_of_likes - 1,
                                                amount_of_dislikes=amount_of_dislikes + 1))
        with utils.database.database as db:
            db.remove_vote(user_id=user_id, message_id=message_id)
            db.add_vote(user_id=user_id, message_id=message_id, vote='dislike')


def register_vote_buttons_handler(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(vote_buttons, aiogram.filters.Regexp(regexp='^like|^dislike'))
