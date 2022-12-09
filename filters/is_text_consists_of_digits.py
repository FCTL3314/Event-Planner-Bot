async def is_text_consists_of_digits(text):
    for char in text.replace(' ', ''):
        if not char.isdigit():
            return False
    return True
