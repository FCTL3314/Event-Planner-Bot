from typing import List


async def create_channel_and_group_strings(channels: List[tuple], groups: List[tuple]):
    result = ''
    channels_indexes = dict()
    for i, channel in enumerate(channels, 1):
        result += f'{i}. {channel[1]}\n'
        channels_indexes[str(i)] = channel[0]
    for i, group in enumerate(groups, len(channels) + 1):
        result += f'{i}. {group[1]}\n'
        channels_indexes[str(i)] = group[0]
    return result, channels_indexes

