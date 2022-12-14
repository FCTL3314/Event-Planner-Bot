import aiogram


def without_photo_keyboard() -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    inline_keyboard_button = aiogram.types.InlineKeyboardButton(text='Без изображения', callback_data='without_picture')
    return inline_keyboard.add(inline_keyboard_button)
