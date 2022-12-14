import aiogram


def send_event_keyboard() -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    send_button = aiogram.types.InlineKeyboardButton(text='📨Отправить', callback_data='send_event')
    cancel_button = aiogram.types.InlineKeyboardButton(text='❌Отменить', callback_data='cancel')
    return inline_keyboard.row(send_button, cancel_button)
