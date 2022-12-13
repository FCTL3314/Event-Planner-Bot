from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateStatisticsStates(StatesGroup):
    get_channels = State()
