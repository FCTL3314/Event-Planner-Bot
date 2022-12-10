def is_survey_answers_correct(text):
    if '@' in text and len(text.split('@')) > 1 and '' not in text.split('@'):
        return True
    return False
