from typing import List


async def create_channels_text(channels: List[tuple], groups: List[tuple]):
    result = ''
    for i, channel in enumerate(channels, 1):
        result += f'{i}. {channel[1]}\n'
    for i, group in enumerate(groups, len(channels) + 1):
        result += f'{i}. {group[1]}\n'
    return result


async def get_channels_indexes(channels: List[tuple], groups: List[tuple]):
    channels_indexes = dict()
    for i, channel in enumerate(channels, 1):
        channels_indexes[str(i)] = channel[0]
    for i, group in enumerate(groups, len(channels) + 1):
        channels_indexes[str(i)] = group[0]
    return channels_indexes

