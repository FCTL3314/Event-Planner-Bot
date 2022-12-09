import aiogram


def send_event_keyboard():
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    inline_keyboard_button = aiogram.types.InlineKeyboardButton(text='Да, всё верно, отправить.',
                                                                callback_data='send_event')
    return inline_keyboard.add(inline_keyboard_button)
