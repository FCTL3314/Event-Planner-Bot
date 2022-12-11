import aiogram


def vote_keyboard(amount_of_likes: int, amount_of_dislikes: int):
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    like_button = aiogram.types.InlineKeyboardButton(text=f'👍🏼 {amount_of_likes}',
                                                     callback_data=f'like {amount_of_likes} {amount_of_dislikes}')
    dislike_button = aiogram.types.InlineKeyboardButton(text=f'👎🏼 {amount_of_dislikes}',
                                                        callback_data=f'dislike {amount_of_likes} {amount_of_dislikes}')
    return inline_keyboard.row(like_button, dislike_button)
