import aiogram


def up_down_counter_keyboard():
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    inline_keyboard_plus_button = aiogram.types.InlineKeyboardButton(text='👍🏼 0', callback_data='up')
    inline_keyboard_minus_button = aiogram.types.InlineKeyboardButton(text='👎🏼 0', callback_data='down')
    inline_keyboard.row(inline_keyboard_plus_button, inline_keyboard_minus_button)
    return inline_keyboard
