import aiogram


def vote_keyboard(likes_count: int, record_count: int, think_count: int, link_button_url: str = None,
                  link_button_name: str = None):
    inline_keyboard = aiogram.types.InlineKeyboardMarkup()
    like_button = aiogram.types.InlineKeyboardButton(text=f'👍🏼 Приду {likes_count}',
                                                     callback_data=f'like')
    record_button = aiogram.types.InlineKeyboardButton(text=f'💫 Запись {record_count}',
                                                       callback_data=f'record')
    think_button = aiogram.types.InlineKeyboardButton(text=f'💤 Думаю {think_count}',
                                                      callback_data=f'think')
    inline_keyboard.row(like_button, record_button, think_button)
    if link_button_url and link_button_name:
        link_button = aiogram.types.InlineKeyboardButton(text=f'{link_button_name}', url=f'{link_button_url}',
                                                         callback_data=f'think')
        inline_keyboard.add(link_button)
    return inline_keyboard
