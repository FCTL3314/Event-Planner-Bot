import aiogram


def without_photo_keyboard():
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    inline_keyboard_button = aiogram.types.InlineKeyboardButton(text='Без кнопки-ссылки',
                                                                callback_data='without_link_button')
    return inline_keyboard.add(inline_keyboard_button)
