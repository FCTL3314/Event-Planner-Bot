import aiogram
import keyboards
import utils

from loader import bot


async def vote_buttons(callback: aiogram.types.CallbackQuery):
    vote = callback.data
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    first_name = callback.from_user.first_name
    last_name = callback.from_user.last_name
    with utils.database.database as db:
        previous_user_vote = db.execute(f'SELECT vote FROM user_votes WHERE (message_id = {message_id}) '
                                        f'AND (user_id = {user_id}) AND (chat_id = {chat_id})')
        fire_button_count = db.execute(f'SELECT fire_button_count FROM events WHERE '
                                       f'(chat_id = {chat_id}) and (message_id = {message_id})')
        think_button_count = db.execute(f'SELECT think_button_count FROM events WHERE '
                                        f'(chat_id = {chat_id}) and (message_id = {message_id})')
        fire_button_limit = db.execute(f'SELECT fire_button_limit FROM events WHERE '
                                       f'(chat_id = {chat_id}) and (message_id = {message_id})')
        link_button_name = db.execute(f'SELECT link_button_name FROM events WHERE '
                                      f'(chat_id = {chat_id}) and (message_id = {message_id})')
        link_button_url = db.execute(f'SELECT link_button_url FROM events WHERE '
                                     f'(chat_id = {chat_id}) and (message_id = {message_id})')
    if vote in ('fire', 'think') and fire_button_count != []:
        fire_button_count = fire_button_count[0][0]
        think_button_count = think_button_count[0][0]
        fire_button_limit = fire_button_limit[0][0]
        link_button_name = link_button_name[0][0]
        link_button_url = link_button_url[0][0]
        if vote == 'fire' and previous_user_vote and previous_user_vote[0][0] != 'fire' and \
                fire_button_count + 1 >= fire_button_limit:
            if link_button_name:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote_limit.vote_limit_keyboard(
                                                        limit=fire_button_limit,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url))
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote_limit.vote_limit_keyboard(
                                                        limit=fire_button_limit))
        elif vote == 'fire' and not previous_user_vote:
            if link_button_name:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count + 1,
                                                        think_button_count=think_button_count,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url))
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count + 1,
                                                        think_button_count=think_button_count,
                                                        link_button_name=link_button_name))
            with utils.database.database as db:
                db.execute(f'UPDATE events SET fire_button_count = {fire_button_count + 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f"INSERT INTO user_votes VALUES ({chat_id}, {message_id}, {user_id}, '{first_name}', "
                           f"'{last_name}', 'fire')")
        elif vote == 'fire' and previous_user_vote[0][0] == 'fire':
            if link_button_name:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count - 1,
                                                        think_button_count=think_button_count,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url))
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count - 1,
                                                        think_button_count=think_button_count))
            with utils.database.database as db:
                db.execute(f'UPDATE events SET fire_button_count = {fire_button_count - 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f'DELETE FROM user_votes WHERE (user_id = {user_id}) AND (chat_id = {chat_id}) AND '
                           f'(message_id = {message_id})')
        elif vote == 'think' and not previous_user_vote:
            if link_button_name:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count,
                                                        think_button_count=think_button_count + 1,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url))
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count,
                                                        think_button_count=think_button_count + 1,
                                                        link_button_name=link_button_name))
            with utils.database.database as db:
                db.execute(f'UPDATE events SET think_button_count = {think_button_count + 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f"INSERT INTO user_votes VALUES ({chat_id}, {message_id}, {user_id}, '{first_name}', "
                           f"'{last_name}', 'think')")
        elif vote == 'think' and previous_user_vote[0][0] == 'think':
            if link_button_name:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count,
                                                        think_button_count=think_button_count - 1,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url))
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count,
                                                        think_button_count=think_button_count - 1,
                                                        link_button_name=link_button_name))
            with utils.database.database as db:
                db.execute(f'UPDATE events SET think_button_count = {think_button_count - 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f'DELETE FROM user_votes WHERE (user_id = {user_id}) AND (chat_id = {chat_id}) AND '
                           f'(message_id = {message_id})')
        elif vote == 'think' and previous_user_vote[0][0] == 'fire':
            if link_button_name:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count - 1,
                                                        think_button_count=think_button_count + 1,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url))
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count - 1,
                                                        think_button_count=think_button_count + 1,
                                                        link_button_name=link_button_name))
            with utils.database.database as db:
                db.execute(f'UPDATE events SET think_button_count = {think_button_count + 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f'UPDATE events SET fire_button_count = {fire_button_count - 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f"UPDATE user_votes SET vote = 'think' WHERE (chat_id = {chat_id}) AND "
                           f"(message_id = {message_id}) AND (user_id = {user_id})")
        elif vote == 'fire' and previous_user_vote[0][0] == 'think':
            if link_button_name:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count + 1,
                                                        think_button_count=think_button_count - 1,
                                                        link_button_name=link_button_name,
                                                        link_button_url=link_button_url))
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                    reply_markup=keyboards.inline.vote.vote_keyboard(
                                                        fire_button_count=fire_button_count + 1,
                                                        think_button_count=think_button_count - 1,
                                                        link_button_name=link_button_name))
            with utils.database.database as db:
                db.execute(f'UPDATE events SET think_button_count = {think_button_count - 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f'UPDATE events SET fire_button_count = {fire_button_count + 1} '
                           f'WHERE (chat_id = {chat_id}) and (message_id = {message_id})')
                db.execute(f"UPDATE user_votes SET vote = 'fire' WHERE (chat_id = {chat_id}) AND "
                           f"(message_id = {message_id}) AND (user_id = {user_id})")
        if vote == 'fire':
            await callback.answer(text='Вы нажали 🔥')
        elif vote == 'think':
            await callback.answer(text='Вы нажали 🤔')


def register_vote_buttons_handler(dp: aiogram.Dispatcher):
    dp.register_callback_query_handler(vote_buttons, aiogram.filters.Regexp(regexp='^fire|^think'))
