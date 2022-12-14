from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateEventStates(StatesGroup):
    get_event_name = State()
    get_event_picture = State()
    get_event_description = State()
    get_vote_limit = State()
    get_link_button_name = State()
    get_link_button_url = State()
    get_channels_to_send = State()
    send_event = State()
