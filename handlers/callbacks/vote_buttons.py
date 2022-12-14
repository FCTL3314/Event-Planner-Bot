import aiogram
import keyboards
import utils

from loader import bot


async def vote_buttons(callback: aiogram.types.CallbackQuery):
    vote = callback.data
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    with utils.database.database as db:
        user_vote = db.get_vote(chat_id=chat_id, message_id=message_id, user_id=user_id)
        likes_count = db.execute(f'SELECT likes_count FROM event_data WHERE '
                                 f'(chat_id = {chat_id}) and (message_id = {message_id})')[0][0]
        record_count = db.execute(f'SELECT record_count FROM event_data WHERE '
                                  f'(chat_id = {chat_id}) and (message_id = {message_id})')[0][0]
        think_count = db.execute(f'SELECT think_count FROM event_data WHERE '
                                 f'(chat_id = {chat_id}) and (message_id = {message_id})')[0][0]
        vote_limit = db.execute(f'SELECT vote_limit FROM event_data WHERE '
                                f'(chat_id = {chat_id}) and (message_id = {message_id})')[0][0]
        link_button_name = db.execute(f'SELECT link_button_name FROM event_data WHERE '
                                      f'(chat_id = {chat_id}) and (message_id = {message_id})')[0][0]
        link_button_url = db.execute(f'SELECT link_button_url FROM event_data WHERE '
                                     f'(chat_id = {chat_id}) and (message_id = {message_id})')[0][0]
    if likes_count >= vote_limit:
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=keyboards.inline.vote_limit.vote_limit_keyboard(
                                                limit=vote_limit))
    elif vote == 'like' and not user_vote:
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count + 1,
                                                    record_count=record_count,
                                                    think_count=think_count,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count + 1,
                                                    record_count=record_count,
                                                    think_count=think_count))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET likes_count = {likes_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.add_vote(chat_id=chat_id, user_id=user_id, message_id=message_id, vote='like')
    elif vote == 'like' and user_vote[0] == 'like':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count - 1,
                                                    record_count=record_count,
                                                    think_count=think_count,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count - 1,
                                                    record_count=record_count,
                                                    think_count=think_count))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET likes_count = {likes_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.remove_vote(chat_id=chat_id, user_id=user_id, message_id=message_id)
    elif vote == 'like' and user_vote[0] == 'record':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count + 1,
                                                    record_count=record_count - 1,
                                                    think_count=think_count,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count + 1,
                                                    record_count=record_count - 1,
                                                    think_count=think_count))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET likes_count = {likes_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f'UPDATE event_data SET record_count = {record_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f"UPDATE event_votes SET vote = 'like' "
                       f"WHERE (chat_id = {chat_id}) and (message_id = {message_id})")
    elif vote == 'like' and user_vote[0] == 'think':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count + 1,
                                                    record_count=record_count,
                                                    think_count=think_count - 1,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count + 1,
                                                    record_count=record_count,
                                                    think_count=think_count - 1))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET likes_count = {likes_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f'UPDATE event_data SET think_count = {think_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f"UPDATE event_votes SET vote = 'like' "
                       f"WHERE (chat_id = {chat_id}) and (message_id = {message_id})")
    elif vote == 'record' and not user_vote:
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count + 1,
                                                    think_count=think_count,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count + 1,
                                                    think_count=think_count))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET record_count = {record_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.add_vote(chat_id=chat_id, user_id=user_id, message_id=message_id, vote='record')
    elif vote == 'record' and user_vote[0] == 'record':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count - 1,
                                                    think_count=think_count,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count - 1,
                                                    think_count=think_count))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET record_count = {record_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.remove_vote(chat_id=chat_id, user_id=user_id, message_id=message_id)
    elif vote == 'record' and user_vote[0] == 'like':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count - 1,
                                                    record_count=record_count + 1,
                                                    think_count=think_count,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count - 1,
                                                    record_count=record_count + 1,
                                                    think_count=think_count))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET likes_count = {likes_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f'UPDATE event_data SET record_count = {record_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f"UPDATE event_votes SET vote = 'record' "
                       f"WHERE (chat_id = {chat_id}) and (message_id = {message_id})")
    elif vote == 'record' and user_vote[0] == 'think':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count + 1,
                                                    think_count=think_count - 1,
                                                    link_button_url=link_button_url,
                                                    link_button_name=link_button_name))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count + 1,
                                                    think_count=think_count - 1))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET record_count = {record_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f'UPDATE event_data SET think_count = {think_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f"UPDATE event_votes SET vote = 'record' "
                       f"WHERE (chat_id = {chat_id}) and (message_id = {message_id})")
    elif vote == 'think' and not user_vote:
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count,
                                                    think_count=think_count + 1,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count,
                                                    think_count=think_count + 1))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET think_count = {think_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.add_vote(chat_id=chat_id, user_id=user_id, message_id=message_id, vote='think')
    elif vote == 'think' and user_vote[0] == 'think':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count,
                                                    think_count=think_count - 1,
                                                    link_button_url=link_button_url,
                                                    link_button_name=link_button_name))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count,
                                                    think_count=think_count - 1))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET think_count = {think_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.remove_vote(chat_id=chat_id, user_id=user_id, message_id=message_id)
    elif vote == 'think' and user_vote[0] == 'like':
        if link_button_name:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count - 1,
                                                    record_count=record_count,
                                                    think_count=think_count + 1,
                                                    link_button_name=link_button_name,
                                                    link_button_url=link_button_url))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count - 1,
                                                    record_count=record_count,
                                                    think_count=think_count + 1))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET think_count = {think_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f'UPDATE event_data SET likes_count = {likes_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f"UPDATE event_votes SET vote = 'think' "
                       f"WHERE (chat_id = {chat_id}) and (message_id = {message_id})")
    elif vote == 'think' and user_vote[0] == 'record':
        if link_button_name:
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                          reply_markup=keyboards.inline.vote.vote_keyboard(
                                              likes_count=likes_count,
                                              record_count=record_count - 1,
                                              think_count=think_count + 1,
                                              link_button_url=link_button_url,
                                              link_button_name=link_button_name))
        else:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                reply_markup=keyboards.inline.vote.vote_keyboard(
                                                    likes_count=likes_count,
                                                    record_count=record_count - 1,
                                                    think_count=think_count + 1))
        with utils.database.database as db:
            db.execute(f'UPDATE event_data SET think_count = {think_count + 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f'UPDATE event_data SET record_count = {record_count - 1} '
                       f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
            db.execute(f"UPDATE event_votes SET vote = 'think' "
                       f"WHERE (chat_id = {chat_id}) and (message_id = {message_id})")


def register_vote_buttons_handler(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(vote_buttons, aiogram.filters.Regexp(regexp='^like|^record|^think'))
