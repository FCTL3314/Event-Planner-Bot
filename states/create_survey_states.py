from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateSurveyStates(StatesGroup):
    get_survey_name = State()
    get_survey_answers = State()
    get_channels_to_send = State()
    send_survey = State()
