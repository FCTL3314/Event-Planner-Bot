import aiogram


def vote_limit_keyboard(limit):
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    limit_filled_button = aiogram.types.InlineKeyboardButton(text=f'❌{limit}/{limit} лимит исчерпан',
                                                             callback_data='limit')
    return inline_keyboard.row(limit_filled_button)
