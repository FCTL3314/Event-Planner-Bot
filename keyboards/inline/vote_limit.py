import aiogram


def vote_limit_keyboard(limit: int, link_button_name=None, link_button_url=None) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    limit_filled_button = aiogram.types.InlineKeyboardButton(text=f'❌{limit}/{limit}❌', callback_data='limit')
    inline_keyboard.row(limit_filled_button)
    if link_button_name:
        inline_keyboard.add(aiogram.types.InlineKeyboardButton(text=link_button_name, url=link_button_url,
                                                               callback_data='link_button'))
    return inline_keyboard
