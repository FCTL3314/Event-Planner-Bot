from aiogram.dispatcher.filters.state import StatesGroup, State


class ClearCommandStates(StatesGroup):
    are_you_sure = State()
