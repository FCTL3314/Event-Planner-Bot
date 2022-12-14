import aiogram


def vote_keyboard(fire_button_count: int, think_button_count: int, link_button_url: str = None,
                  link_button_name: str = None)  -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    like_button = aiogram.types.InlineKeyboardButton(text=f'🔥 {fire_button_count}',
                                                     callback_data=f'fire')
    record_button = aiogram.types.InlineKeyboardButton(text=f'🤔 {think_button_count}',
                                                       callback_data=f'think')
    inline_keyboard.row(like_button, record_button)
    if link_button_url and link_button_name:
        link_button = aiogram.types.InlineKeyboardButton(text=f'{link_button_name}', url=f'{link_button_url}',
                                                         callback_data=f'link_button')
        inline_keyboard.add(link_button)
    return inline_keyboard
