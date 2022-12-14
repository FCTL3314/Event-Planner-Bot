from typing import List


async def create_channels_text(channels: List[tuple], groups: List[tuple]):
    result = ''
    if channels:
        for i, channel in enumerate(channels, 1):
            result += f'{i}. {channel[1]}\n'
    if groups:
        for i, group in enumerate(groups, len(channels) + 1):
            result += f'{i}. {group[1]}\n'
    return result


async def get_channels_indexes(channels: List[tuple], groups: List[tuple]):
    channels_indexes = dict()
    if channels:
        for i, channel in enumerate(channels, 1):
            channels_indexes[str(i)] = channel[0]
    if groups:
        for i, group in enumerate(groups, len(channels) + 1):
            channels_indexes[str(i)] = group[0]
    return channels_indexes


async def create_users_vote_text(users, emoji):
    result = f'<b>Пользователи которые нажали</b> {emoji}:\n'
    for i, data in enumerate(users, 1):
        result += f'{i}. <a href="tg://user?id={data[0]}">{data[1]} {data[2]}</a>\n'
    return result
