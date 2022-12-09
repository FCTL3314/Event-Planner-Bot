async def is_channel_numbers_correct(text, channels_ids_dict):
    for char in text.split(' '):
        if char not in channels_ids_dict:
            return False
    return True
