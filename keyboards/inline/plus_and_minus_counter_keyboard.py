import aiogram


def plus_and_minus_counter_keyboard():
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    inline_keyboard_plus_button = aiogram.types.InlineKeyboardButton(text='➕', callback_data='plus')
    inline_keyboard_minus_button = aiogram.types.InlineKeyboardButton(text='➖', callback_data='minus')
    inline_keyboard.row(inline_keyboard_plus_button, inline_keyboard_minus_button)
    return inline_keyboard
